import argparse
from stix2 import MemoryStore
import os
import requests
import pandas as pd

import mitreattack.attackToExcel.stixToDf as stixToDf


INVALID_CHARACTERS = ["\\", "/", "*", "[", "]", ":", "?"]
SUB_CHARACTERS = ["\\", "/"]


def get_stix_data(domain, version=None, remote=None):
    """
    download the ATT&CK STIX data for the given domain and version from MITRE/CTI (or just domain if a remote workbench
    is specified).
    :param domain: the domain of ATT&CK to fetch data from, e.g "enterprise-attack"
    :param version: the version of attack to fetch data from, e.g "v8.1". If omitted, returns the latest version
                    (not used for invocations that use remote)
    :param remote: optional url to a ATT&CK workbench instance. If specified, data will be retrieved from the target
                    Workbench instead of MITRE/CTI
    :returns: a MemoryStore containing the domain data
    """
    if remote:  # Using Workbench Instance
        if ':' not in remote[6:]:
            remote += ":3000"
        if not remote.startswith('http'):
            remote = 'http://' + remote
        url = f"{remote}/api/stix-bundles?domain={domain}&includeRevoked=true&includeDeprecated=true"
        stix_json = requests.get(url).json()
        return MemoryStore(stix_json)
    else:  # Using MITRE/CTI
        if version:
            url = f"https://raw.githubusercontent.com/mitre/cti/ATT%26CK-{version}/{domain}/{domain}.json"
        else:
            url = f"https://raw.githubusercontent.com/mitre/cti/master/{domain}/{domain}.json"

        stix_json = requests.get(url).json()
        return MemoryStore(stix_data=stix_json["objects"])


def build_dataframes(src, domain):
    """
    build pandas dataframes for each attack type, and return a dictionary lookup for each type to the relevant dataframe
    :param src: MemoryStore or other stix2 DataSource object
    :param domain: domain of ATT&CK src corresponds to, e.g "enterprise-attack"
    :returns: a dict lookup of each ATT&CK type to dataframes for the given type to be ingested by write_excel
    """
    df = {
            "techniques": stixToDf.techniquesToDf(src, domain),
            "tactics": stixToDf.tacticsToDf(src, domain),
            "software": stixToDf.softwareToDf(src, domain),
            "groups": stixToDf.groupsToDf(src, domain),
            "mitigations": stixToDf.mitigationsToDf(src, domain),
            "matrices": stixToDf.matricesToDf(src, domain),
            "relationships": stixToDf.relationshipsToDf(src)
        }
    # get each ATT&CK type
    if domain == 'enterprise-attack':
        df["datasources"] = stixToDf.sourcesToDf(src, domain)
    return df


def write_excel(dataframes, domain, version=None, outputDir="."):
    """
    given a set of dataframes from build_dataframes, write the ATT&CK dataset to output directory
    :param dataframes: pandas dataframes as built by build_dataframes
    :param domain: domain of ATT&CK the dataframes correspond to, e.g "enterprise-attack"
    :param version: optional, the version of ATT&CK the dataframes correspond to, e.g "v8.1".
                    If omitted, the output files will not be labelled with the version number
    :param outputDir: optional, the directory to write the excel files to. If omitted writes to a
                      subfolder of the current directory depending on specified domain and version
    :returns: a list of filepaths corresponding to the files written by the function
    """

    print("writing formatted files... ", end="", flush=True)
    # master list of files that have been written
    written_files = []
    # set up output directory
    if version:
        domainVersionString = f"{domain}-{version}"
    else:
        domainVersionString = domain
    outputDirectory = os.path.join(outputDir, domainVersionString)
    if not os.path.exists(outputDirectory):
        os.makedirs(outputDirectory)
    # master dataset file
    master_fp = os.path.join(outputDirectory, f"{domainVersionString}.xlsx")
    master_writer = pd.ExcelWriter(master_fp, engine='xlsxwriter')
    citations = pd.DataFrame()  # master list of citations
    # write individual dataframes and add to master writer
    for objType in dataframes:
        if objType != "matrices":
            # write the dataframes for the object type into named sheets
            fp = os.path.join(outputDirectory, f"{domainVersionString}-{objType}.xlsx")
            obj_writer = pd.ExcelWriter(fp)
            for dfname in dataframes[objType]:
                dataframes[objType][dfname].to_excel(obj_writer, sheet_name=dfname, index=False)
            obj_writer.save()
            written_files.append(fp)

            # add citations to master citations list
            if "citations" in dataframes[objType]:
                citations = citations.append(dataframes[objType]["citations"])

            # add main df to master dataset
            dataframes[objType][objType].to_excel(master_writer, sheet_name=objType, index=False)
        else:  # handle matrix special formatting
            fp = os.path.join(outputDirectory, f"{domainVersionString}-{objType}.xlsx")
            matrix_writer = pd.ExcelWriter(fp, engine='xlsxwriter')
            combined = dataframes[objType][0] + dataframes[objType][1]  # Combine both matrix types
            for matrix in combined:  # some domains have multiple matrices
                # name them accordingly if there are multiple
                sheetname = "matrix" if len(combined) == 1 else matrix["name"] + " matrix"
                for character in INVALID_CHARACTERS:
                    sheetname = sheetname.replace(character, " or " if character in SUB_CHARACTERS else " ")

                if len(sheetname) > 31:
                    sheetname = sheetname[0:28] + "..."
                listing = []
                if matrix in dataframes[objType][0]:  # avoid printing subtype matrices to the master file
                    matrix["matrix"].to_excel(master_writer, sheet_name=sheetname,
                                              index=False)  # write unformatted matrix data to master file
                    listing.append(master_writer)

                matrix["matrix"].to_excel(matrix_writer, sheet_name=sheetname,
                                          index=False)  # write unformatted matrix to matrix file
                listing.append(matrix_writer)

                # for each writer, format the matrix for readability
                for writer in listing:
                    # define column border styles
                    borderleft = writer.book.add_format({"left": 1, "shrink": 1})
                    borderright = writer.book.add_format({"right": 1, "shrink": 1})
                    formats = {}  # formats only need to be defined once: pointers stored here for subsequent uses
                    sheet = writer.sheets[sheetname]

                    sheet.set_column(0, matrix["columns"],
                                     width=20)  # set all columns to 20 width, and add text shrinking to fit

                    # merge supertechniques and tactic headers if sub-techniques are present on a tactic
                    for mergeRange in matrix["merge"]:
                        if mergeRange.format:  # sometimes merge ranges have formats to add to the merged range
                            if mergeRange.format["name"] not in formats:  # add format to book if not defined
                                formats[mergeRange.format["name"]] = writer.book.add_format(mergeRange.format["format"])
                            theformat = formats[mergeRange.format["name"]]  # get saved format if already added
                            # tactic header merge has additional behavior
                            if mergeRange.format["name"] == "tacticHeader":
                                # also set border for entire column for grouping
                                sheet.set_column(
                                    mergeRange.leftCol - 1,
                                    mergeRange.leftCol - 1,
                                    width=20,  # set column widths to make matrix more readable
                                    cell_format=borderleft  # left border around tactic
                                )
                                sheet.set_column(
                                    mergeRange.rightCol - 1,
                                    mergeRange.rightCol - 1,
                                    width=20,  # set column widths to make matrix more readable
                                    cell_format=borderright  # right border around tactic
                                )
                        else:
                            theformat = None  # no format
                        sheet.merge_range(mergeRange.to_excel_format(), mergeRange.data, theformat)  # apply the merge

            matrix_writer.save()  # save the matrix data
            written_files.append(fp)
            # end of matrix sheet writing

    # remove duplicate citations and add sheet to master file
    citations.drop_duplicates(subset="reference", ignore_index=True).sort_values("reference")\
        .to_excel(master_writer, sheet_name="citations", index=False)
    # write the master file
    master_writer.save()
    written_files.append(master_fp)
    print("done")
    print("files created:")
    for thefile in written_files:
        print("\t", thefile)
    return written_files


def export(domain="enterprise-attack", version=None, outputDir=".", remote=None):
    """
    Download ATT&CK data from MITRE/CTI and convert it to excel spreadsheets
    :param domain: the domain of ATT&CK to download, e.g "enterprise-attack"
    :param version: optional, the version of ATT&CK to download, e.g "v8.1". If omitted will build the current version
                    of ATT&CK
    :param outputDir: optional, the directory to write the excel files to. If omitted writes to a
                      subfolder of the current directory depending on specified domain and version
    :param remote: optional, the URL of a remote ATT&CK Workbench instance to connect to for stix data
    """
    # build dataframes
    dataframes = build_dataframes(get_stix_data(domain, version, remote), domain)
    write_excel(dataframes, domain, version, outputDir)


def main():
    parser = argparse.ArgumentParser(
        description="Download ATT&CK data from MITRE/CTI and convert it to excel spreadsheets"
    )
    parser.add_argument("-domain",
                        type=str,
                        choices=["enterprise-attack", "mobile-attack", "ics-attack"],
                        default="enterprise-attack",
                        help="which domain of ATT&CK to convert"
                        )
    parser.add_argument("-version",
                        type=str,
                        help="which version of ATT&CK to convert. If omitted, builds the latest version"
                        )
    parser.add_argument("-output",
                        type=str,
                        default=".",
                        help="output directory. If omitted writes to a subfolder of the current directory depending on "
                             "the domain and version"
                        )
    parser.add_argument("-remote",
                        type=str,
                        default=None,
                        help="remote url of an ATT&CK workbench server. If omitted, stix data will be acquired from the"
                             " official ATT&CK Taxii server (cti-taxii.mitre.org)"
                        )
    args = parser.parse_args()

    export(args.domain, args.version, args.output, args.remote)


if __name__ == '__main__':
    main()
