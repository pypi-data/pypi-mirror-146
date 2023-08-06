import json
import os
import pytest
from docparser.doc_parser_factory import DocParserFactory

# from tests.excel_config import ExcelConfig as Config
doc1_config = {}
test_config = {
    "id": "CMA",
    "name": "CMA config",
    "kv": {
        "VESSEL": {
            "position_pattern": [
                "^VESSEL:"
            ],
            "value_pattern": [
                "(?P<Vessel>[\\w\\W]*?)(?:\\r\\n|\\n|$)"
            ],
            "repeat_count": 1,
            "find_mode": "h",
            "separator_mode": "regex",
            "is_split_cell": 0,
            "split_pattern": [
                ""
            ],
            "action": [
                {
                    "keyword": "VesselName",
                    "key": "Vessel"
                }
            ]
        },
        "VOYAGE": {
            "position_pattern": [
                "^VOYAGE:"
            ],
            "value_pattern": [
                "VOYAGE\\s*:\\s*(?P<VOYAGE>[\\w\\W]*)"
            ],
            "repeat_count": 1,
            "find_mode": "default",
            "separator_mode": "regex",
            "is_split_cell": 0,
            "split_pattern": [
                ""
            ],
            "action": [
                {
                    "keyword": "VoyageNo",
                    "key": "VOYAGE"
                }
            ]
        },
        "POD ETA": {
            "position_pattern": [
                "^POD ETA"
            ],
            "value_pattern": [
                "POD\\s*ETA\\s*:\\s*(?P<ETA>\\d+/\\d+/\\d+)(?:\\r\\n|\\n)"
            ],
            "repeat_count": 1,
            "find_mode": "default",
            "separator_mode": "regex",
            "is_split_cell": 0,
            "split_pattern": [
                ""
            ],
            "action": [
                {
                    "keyword": "EstimatedArrivalDate",
                    "key": "ETA"
                }
            ]
        },
        "DeliveryPlaceName": {
            "position_pattern": [
                "^OPERATIONAL LOAD PORT"
            ],
            "value_pattern": [
                "[\\w\\W]*?(?:\\n|\\r\\n|)(?P<DELIVERY>.*)"
            ],
            "repeat_count": 1,
            "find_mode": "h",
            "separator_mode": "regex",
            "is_split_cell": 0,
            "split_pattern": [
                ""
            ],
            "action": [
                {
                    "keyword": "DeliveryPlaceName",
                    "key": "DELIVERY"
                }
            ]
        },
        "BillOfLadingsId": {
            "position_pattern": [
                "^Please clear your cargo",
                "Please Pay freight against "
            ],
            "value_pattern": [
                "[\\w\\W]*?(?P<billoflading>[a-zA-Z]{4,}\\d{5,}[a-zA-Z]*)\\s*",
                "[\\w\\W]*?(?P<billoflading>[a-zA-Z]{4}\\s*[a-zA-Z]{3,}\\d{5,}[a-zA-Z]*)\\s*((Waybill)|(Negotiable))"
            ],
            "repeat_count": 1,
            "find_mode": "default",
            "separator_mode": "regex",
            "is_split_cell": 0,
            "split_pattern": [
                ""
            ],
            "action": [
                {
                    "keyword": "BillOfLadingsId",
                    "key": "billoflading"
                }
            ]
        },
        "BillOfLadingsId1": {
            "position_pattern": [
                "^Please[\\w\\W]*BILL\\s*TYPE$",
                "^SCAC\\s{2,}B/L\\s*#$"
            ],
            "value_pattern": [
                "(?P<billoflading>[a-zA-Z]{4,}\\s*[a-zA-Z]*\\d{5,}[a-zA-Z]*)$",
            ],
            "repeat_count": 1,
            "find_mode": "v",
            "separator_mode": "regex",
            "is_split_cell": 0,
            "split_pattern": [
                ""
            ],
            "action": [
                {
                    "keyword": "BillOfLadingsId",
                    "key": "billoflading"
                }
            ]
        }
    },
    "table": {
        "containers": {
            "position_pattern": [
                "^CONTAINER\\s*#"
            ],
            "separator": " ",
            "find_mode": "v",
            "separator_mode": "regex",
            "column": [
                "ContainerNo"
            ],
            "behaviors": [
                {
                    "over_action": "row",
                    "value_pattern": [
                        "(?P<col_1>([a-zA-Z]{4,}\\d{7,}\\s*)*)"
                    ],
                    "action": []
                }
            ]
        }
    },
    "data_type_format": {
        "VoyageNo": {
            "data_type": "str",
            "filter": "r([/\\s])"
        },
        "EstimatedArrivalDate": {
            "data_type": "time",
            "format": "%m/%d/%Y",
            "filter": ""
        },
        "BillOfLadingsId": {
            "data_type": "str",
            "filter": "(\\s)"
        }
    },
    # "address_repair": {
    #     "db": {
    #         "pub": {
    #             "user": "co",
    #             "pwd": "Co&23@2332$22",
    #             "server": "db.dev.com:1433",
    #             "database": "CO_PUB"
    #         }
    #     },
    #     "repairs": [
    #         {
    #             "key": "DeliveryPlaceName",
    #             "db_key": "pub",
    #             "sql": "SELECT  [FullName],[LocalName],[name],[code],[Id] from Places WHERE IsDeleted = 0 and IsOcean = 1 and IsValid = 1 and ([FullName] like '%${value}%' or charindex([FullName],'${value}')> 0) ;",
    #             "column": [
    #                 0,
    #                 1,
    #                 2,
    #                 3
    #             ],
    #             "value": 4,
    #             "mapping": "DeliveryPlaceId",
    #             "old_val_handle": "empty"
    #         }
    #     ]
    # }
}

config_names = []

for k, v in test_config.get('kv').items():
    action = v.get('action')
    for _item in action:
        config_names.append((k, _item.get("keyword")))


class TestExcelDocumentParser:

    def test_excel_file_parse(self):
        """
        单文件测试
        :return:
        """
        name = "cma".upper()

        doc1_config["id"] = f"AN_{name}_"

        test_config["id"] = name
        test_config["name"] = f"{name} config"
        doc1_config["parse"] = test_config
        # print(test_config)
        print(json.dumps(doc1_config))
        str_dir = f"C:\\Users\\APing\\Desktop\\temp\\{name}"
        files = os.listdir(str_dir)
        size = 0
        f_list = []
        for f in files:
            # if f != "bl2687093129.xlsx":
            #     continue
            if f.endswith('.xlsx') and not f.startswith('~'):
                # factory = DocParserFactory.create("excel2",
                #                                   r"C:\Users\APing\Desktop\temp\cma\ARR_JXTL311318.xlsx",
                #                                   test_config)
                factory = DocParserFactory.create("excel2", os.path.join(str_dir, f), test_config)
                result, errors = factory.parse()
                size += 1
                if len(result) == 0:
                    f_list.append({f: errors})
                else:
                    err_list = []
                    for nm in config_names:
                        v1 = result[0].get(nm[1])
                        if (v1 is None or v1 == "") and len(errors[0]) > 0 and len(
                                [x for x in errors[0].keys() if x.find(nm[0]) > -1]) > 0:
                            err_list.append(nm[1])
                            break
                    if len(err_list) > 0:
                        f_list.append({f: (err_list, errors)})

                print(f, result, errors)
        print(f"一共解析文件数量：{size}, err-size: {len(f_list)}")
        for _nm in f_list:
            print(_nm)
    # def test_excel_dir_parse(self):
    #     """
    #     测试文件夹下的拥有对应名称配置的excel文件
    #     :return:
    #     """
    #     path = os.getcwd() + "\\files"
    #     dirs = os.listdir(path)
    #     for file in dirs:
    #         name = file.split(".")[0]
    #         if ".xlsx" in file:
    #             _config = Config.get_config(name.lower())
    #             if _config is None:
    #                 continue
    #             factory = DocParserFactory.create("excel2", "%s\\%s.xlsx" % (path, name.lower()), _config)
    #             result, errors = factory.parse()
    #             print("=========================", file, "========================")
    #             print(_config)
    #             print(path + file)
    #             print(result)
    #             print(errors)
    #             print("------------------------------------------------------------")
    #             print("\r\n\r\n")


if __name__ == '__main__':
    pytest.main("-q --html=report.html")
