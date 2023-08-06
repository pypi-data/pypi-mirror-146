# -*- coding: utf8 -*-
# Copyright (c) 2021-2021 Pinclr, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import logging
import random
from datetime import datetime
from typing import List
import requests
from TLSSigAPIv2 import TLSSigAPIv2

TCIM_API_BASE = "https://console.tim.qq.com/v4"


class MyLogger(object):

    @staticmethod
    def get_logger(class_name):
        logging_level = logging.INFO
        my_logger = logging.getLogger(class_name)
        my_logger.setLevel(logging_level)
        handler = logging.StreamHandler()
        handler.setLevel(logging_level)
        formatter = logging.Formatter('%(asctime)s %(filename)s:%(lineno)d [%(levelname)s]%(message)s')
        handler.setFormatter(formatter)
        my_logger.addHandler(handler)
        return my_logger


logger = MyLogger.get_logger(__name__)


class MessageText(object):
    """
    text message
    """

    def __init__(self, message):
        self.MsgType = "TIMTextElem"
        self.MsgContent = {
            "Text": message
        }


class MessageFile(object):
    """
    file message
    """

    def __init__(self, file_url: str, file_size: int, file_name: str):
        self.MsgType = "TIMFileElem"
        self.MsgContent = {
            "Url": file_url,
            "FileSize": file_size,
            "FileName": file_name,
            "Download_Flag": 2
        }


class MessageObj(object):

    def __init__(
            self,
            from_account: str,
            to_account: str,
            text_messages: List[MessageText]=[],
            attachment_messages: List[MessageFile]=[], sync_machine: int = 1):
        self.From_Account = from_account
        self.To_Account = to_account
        self.SyncOtherMachine = sync_machine
        self.MsgRandom = random.randint(0, 4294967295)
        self.MsgBody = []
        for text_message in text_messages:
            self.MsgBody.append(text_message.__dict__)

        for attachment_message in attachment_messages:
            self.MsgBody.append(attachment_message.__dict__)


class BatchMessageObj(object):
  def __init__(
          self,
          from_account: str,
          to_account:List[str],
          text_messages: List[MessageText] = [],
          attachment_messages: List[MessageFile] = [], sync_machine: int = 1):
    self.From_Account = from_account
    self.To_Account = to_account
    self.SyncOtherMachine = sync_machine
    self.MsgRandom = random.randint(0, 4294967295)
    self.MsgBody = []
    for text_message in text_messages:
      self.MsgBody.append(text_message.__dict__)

    for attachment_message in attachment_messages:
      self.MsgBody.append(attachment_message.__dict__)






class FriendObj(object):
    """
    Friend Object
    Attributes
      to_account: target user id
      add_source: user from where
      group_name
      remark

    """

    def __init__(self, to_account, add_source, remark="", group_name=""):
        """
        :param to_account: 目标用户 必填
        :param remark:     备注
        :param add_source  好友来源：web,android ios
        :param group_name: 用户分组
        """
        self.To_Account = to_account
        self.Remark = remark
        self.GroupName = group_name
        self.AddSource = "AddSource_Type_{}".format(add_source)


class SnsItemObj(object):
    """
    SnsItemObj
    Attributes
      tag:
          Group:Array  user group  value: [] 分组信息
          Remark：user remark：    value:str 好友备注
          AddSource：user source   value:str
          AddWording：好友附言  value:str
          AddTime：user time stamp  value:int
    """

    def __init__(self, tag: str, value: str):
        self.Tag = "Tag_SNS_IM_{}".format(tag)
        self.Value = value


class UpdateFriendObj(object):
    """

    update user object
    """

    def __init__(self, to_account, sns_items: List[SnsItemObj]):
        self.To_Account = to_account
        SnsItem = []
        for sns_item in sns_items:
            SnsItem.append(sns_item.__dict__)
        self.SnsItem = SnsItem


# def Resposne(ActionStatus=None, ErrorInfo=None, ErrorCode=None,
#              FailAccounts=None, ResultItem=None, UserDataItem=None,
#              FriendNum=None, NextStartIndex=None, CompleteFlag=None,
#              Fail_Account=None,ErrorDisplay=None,ResultCode=None):
#   """
#   :param ActionStatus: 请求处理的结果，OK 表示处理成功，FAIL 表示失败
#   :param ErrorInfo:错误信息
#   :param ErrorCode:错误码，0表示成功，非0表示失败
#   :param:ResultItem: 单个帐号的结果对象数组
#   :param FailAccounts:失败账户
#   :param: UserDataItem: 好友信息
#   :param: FriendNum:好友数
#   :param:NextStartIndex:分页接口下一页的起始位置
#   :param: CompleteFlag:分页的结束标识，非0值表示已完成全量拉取
#   :return:
#   """
#   result = {}
#   result["action_status"] = ActionStatus
#   result["error_info"] = ErrorInfo
#   result["err_code"] = ErrorCode
#   result["faile_accounts"] = FailAccounts
#   result["result_item"] = ResultItem
#   result["userdata_item"] = UserDataItem
#   result["friend_num"] = FriendNum
#   result["next_start_index"] = NextStartIndex
#   result["complate_flag"] = CompleteFlag
#   result["faile_account"] = Fail_Account
#   result["err"]
#
#
#   return result


class TCIMClient(object):
    """
    Tecent Im Rest API Client

    Attributes
      sdk_id: im sdk id
      key:IM im sdk secret key
      admin: im sdk admin user id
      tencent_url: tencent im rest url
      expire_time: user sig expire time(seconds)


    """

    def __init__(self, sdk_id, key, admin, tencent_url=TCIM_API_BASE, expire_time=60 * 5):
        """
        :param sdk_id: IM SDK ID
        :param key:    IM SDK SECRET KEY
        :param admin:  ADMIN
        :param tencent_url: tencent rest url
        :param expire_time:   expire time
        """
        self.sdk_id = sdk_id
        self.key = key
        self.admin = admin
        self.tecent_url = tencent_url
        self.expire_time = expire_time
        self.next_time = datetime.now()
        self.user_sig = None

    def get_user_sig(self, user_id: str, expire_time: int = 180 * 86400):
        """
        generate user sig
        :param user_id: user id
        :param expire_time: expire time
        :return: user_sig
        """

        api = TLSSigAPIv2(self.sdk_id, self.key)
        sig = api.gen_sig(user_id, expire_time)
        return sig


    def _gen_query(self):
        """
    generate rest url
    """
        current_time = datetime.now()

        # 计算时间：如果大于登陆5分钟，则重新生成user_sig
        if self.user_sig == None or (current_time - self.next_time).seconds >= self.expire_time:
            self.user_sig = self.get_user_sig(self.admin, self.expire_time)
            self.next_time = current_time

        querys = {}
        querys["sdkappid"] = self.sdk_id
        querys["identifier"] = self.admin
        querys["usersig"] = self.user_sig
        querys["random"] = random.randint(0, 4294967295)
        querys["contenttype"] = "json"
        return querys

    def add_single_user(self, user_id: str, nick_name: str, face_url: str):
        """
        add user to im server
        https://cloud.tencent.com/document/product/269/1608
        :param user_id
        :param nick_name:
        :param face_url:
        :return: response
        response.content:
        {
            "ActionStatus":"OK",  # if "OK" means success else "Fail" means fail
            "ErrorInfo":"",
            "ErrorCode":0
        }
        """
        rest_url = "{}/im_open_login_svc/account_import".format(self.tecent_url)

        data = {}
        try:
            data["UserID"] = user_id
            data["Nick"] = nick_name
            data["FaceUrl"] = face_url
            query = self._gen_query()
            return requests.post(rest_url, params=query, data=json.dumps(data))
        except Exception as e:
            logger.error("add user failed:{}".format(e))
            return None

    def batch_add_users(self, user_ids: List[str]):

        """
        batch add users to im server
        https://cloud.tencent.com/document/product/269/4919
        :param user_ids:  list of user_ids eg: ["user0","user1"]
        :return:response
        response.content
        {
            "ActionStatus": "OK", #if "OK" means success else "Fail" means fail
            "ErrorCode": 0,
            "ErrorInfo": "",
            "FailAccounts": [   // List of accounts that failed to be imported to im server
                "test3",
                "test4"
            ]
        }
        """
        try:
            rest_url = "{}/im_open_login_svc/multiaccount_import".format(self.tecent_url)
            data = {}
            data["Accounts"] = user_ids
            query = self._gen_query()
            return requests.post(rest_url, params=query, data=json.dumps(data))
        except Exception as e:
            logger.error("batch add user failed:{}".format(e))
            return None

    def del_user(self, user_ids: List[str]):

        """
          delete user in im server
          https://cloud.tencent.com/document/product/269/36443
          :param user_ids: list of user_ids eg: ["user0","user1"]
          :return:response
          response.content
          {
              "ActionStatus": "OK",
              "ErrorCode": 0,
              "ErrorInfo": "",
              "ResultItem": [
                  {
                      "ResultCode": 0,   # if "0" means success  else  means fail
                      "ResultInfo": "",  # error info
                      "UserID": "UserID_1"
                  },
                  {
                      "ResultCode": 70107,
                      "ResultInfo": "Err_TLS_PT_Open_Login_Account_Not_Exist",
                      "UserID": "UserID_2"
                  }
              ]
          }
        """
        rest_url = "{}/im_open_login_svc/account_delete".format(self.tecent_url)
        data = {}
        DeleteItem = []
        try:
            for user_id in user_ids:
                tmp_map = {}
                tmp_map["UserID"] = user_id
                DeleteItem.append(tmp_map)

            data["DeleteItem"] = DeleteItem
            query = self._gen_query()
            return requests.post(rest_url, params=query, data=json.dumps(data))
        except Exception as e:

            logger.error("delete user failed:{}".format(e))
            return None

    def search_user(self, user_ids: List[str]):

        """
          search user
          https://cloud.tencent.com/document/product/269/38417
          :param user_ids: list of user_ids eg: ["user0","user1"]
          :return: response
          response.content
          {
              "ActionStatus": "OK",
              "ErrorCode": 0,
              "ErrorInfo": "",
              "ResultItem": [
                  {
                      "UserID": "UserID_1",
                      "ResultCode": 0,     # if "0" means success  else  means fail
                      "ResultInfo": "",
                      "AccountStatus": "Imported"  # "Import" means this user_id is in im server
                  },
                  {
                      "UserID": "UserID_2",
                      "ResultCode": 0,
                      "ResultInfo": "",
                      "AccountStatus": "NotImported"  # "NotImported" means this user_id is not in im server
                  }
              ]
          }
        """
        rest_url = "{}/im_open_login_svc/account_check".format(self.tecent_url)
        data = {}
        CheckItem = []
        try:
            for user_id in user_ids:
                tmp_map = {}
                tmp_map["UserID"] = user_id
                CheckItem.append(tmp_map)

            data["CheckItem"] = CheckItem
            query = self._gen_query()
            return requests.post(rest_url, params=query, data=json.dumps(data))

        except Exception as e:
            logger.error("search user failed:{}".format(e))
            return None

    def abolition_user_sig(self, user_id):
        """
        login status of invalid account
        https://cloud.tencent.com/document/product/269/3853
        :param user_id:
        :return: response
        response.content
        {
            "ActionStatus":"OK",
            "ErrorInfo":"",
            "ErrorCode":0
        }

        """
        rest_url = "{}/im_open_login_svc/kick".format(self.tecent_url)
        data = {}
        data["UserID"] = user_id
        try:
            query = self._gen_query()
            return requests.post(rest_url, params=query, data=json.dumps(data))
        except Exception as e:
            logger.error("abolish user sig failed:{} ".format(e))
            return None

    def check_user_online(self, user_ids: List[str]):
        """
        check user status
        https://cloud.tencent.com/document/product/269/2566
        :param user_ids:list of user_ids eg: ["user0","user1"]
        :return:response
        response.content
        {
            "ActionStatus": "OK",
            "ErrorInfo": "",
            "ErrorCode": 0,
            "QueryResult": [
                {
                    "To_Account": "id1",
                    "Status": "Online",
                    "Detail": [
                        {
                            "Platform": "iPhone",
                            "Status": "PushOnline"
                        },
                        {
                            "Platform": "Web",
                            "Status": "Online"
                        }
                    ]
                },
                {
                    "To_Account": "id2",
                    "Status": "Offline",
                }
            ],
            "ErrorList": [
                {
                    "To_Account": "id4",
                    "ErrorCode": 70107
                }
            ]
            }

        """
        rest_url = "{}/openim/query_online_status".format(self.tecent_url)
        data = {}
        try:
            data["IsNeedDetail"] = 1
            data["To_Account"] = user_ids
            query = self._gen_query()
            return requests.post(rest_url, params=query, data=json.dumps(data))
        except Exception as e:
            logger.error("check user status failed:{}".format(e))
            return None

    def add_friend(self, from_account: str, friends: List[FriendObj]):
        """
        add friend
        https://cloud.tencent.com/document/product/269/1643
        :param from_account: 需要添加好友的账户
        :param friends: need to be added  [FriendObj]
        :return: response
        response.content
        {
            "ResultItem":
            [
                {
                    "To_Account":"id1",
                    "ResultCode":0,
                    "ResultInfo":""
                },
                {
                    "To_Account":"id2",
                    "ResultCode":30006,
                    "ResultInfo":"Err_SNS_FriendAdd_Unpack_Profile_Data_Fail"
                },
                {
                    "To_Account":"id3",
                    "ResultCode":30002,
                    "ResultInfo":"Err_SNS_FriendAdd_SdkAppId_Illegal"
                }
            ],
            "Fail_Account":["id2","id3"],
            "ActionStatus":"OK",
            "ErrorCode":0,
            "ErrorInfo":"",
            "ErrorDisplay":""
        }

        """
        rest_url = "{}/sns/friend_add".format(self.tecent_url)
        data = {}
        data["From_Account"] = from_account
        AddFriendItem = []
        try:
            for friend in friends:
                AddFriendItem.append(friend.__dict__)
            data["AddFriendItem"] = AddFriendItem
            data["AddType"] = "Add_Type_Both"
            data["ForceAddFlags"] = 1
            query = self._gen_query()
            return requests.post(rest_url, params=query, data=json.dumps(data))
        except Exception as e:
            logger.error("add friend failed:{}".format(e))
            return None

    def delete_friends(
            self, from_account: str, to_accounts: List[str], delete_type="Delete_Type_Both"
    ):
        """
        delete friends
        https://cloud.tencent.com/document/product/269/1644
        :param from_account
        :param to_accounts: list of user ids
        :param delete_type: Delete_Type_Both or Delete_Type_Single
        :return: response
        response.content
        {
            "ResultItem":
            [
                {
                    "To_Account":"id1",
                    "ResultCode":0,
                    "ResultInfo":""
                },
                {
                    "To_Account":"id2",
                    "ResultCode":0,
                    "ResultInfo":""
                },
                {
                    "To_Account":"id3",
                    "ResultCode":0,
                    "ResultInfo":""
                }
            ],
            "ActionStatus":"OK",
            "ErrorCode":0,
            "ErrorInfo":"0",
            "ErrorDisplay":""
        }

        """
        rest_url = "{}/sns/friend_delete".format(self.tecent_url)
        data = {}
        try:
            data["From_Account"] = from_account
            data["To_Account"] = to_accounts
            data["DeleteType"] = delete_type
            query = self._gen_query()
            return requests.post(rest_url, params=query, data=json.dumps(data))
        except Exception as e:
            logger.error("delete user failed:{}".format(e))
            return None

    def update_friend(self, from_account: str, update_objs: List[UpdateFriendObj]):
        """
        update friend  relational link data
        https://cloud.tencent.com/document/product/269/12525
        :param from_account:
        :param update_objs: list[UpdateFriendObj]
        :return: response
        response.content
        {
            "ResultItem":
            [
                {
                    "To_Account":"id1",
                    "ResultCode":0,
                    "ResultInfo":""
                },
                {
                    "To_Account":"id2",
                    "ResultCode":30011,
                    "ResultInfo":"Err_SNS_FriendUpdate_Group_Num_Exceed_Threshold"
                },
                {
                    "To_Account":"id3",
                    "ResultCode":30002,
                    "ResultInfo":"Err_SNS_FriendImport_SdkAppId_Illegal"
                }
            ],
            "Fail_Account":["id2","id3"],
            "ActionStatus":"OK",
            "ErrorCode":0,
            "ErrorInfo":"",
            "ErrorDisplay":""
        }
        """

        rest_url = "{}/sns/friend_update".format(self.tecent_url)
        data = {}
        try:
            updateItems = []
            for update_obj in update_objs:
                updateItems.append(update_obj.__dict__)
            data["From_Account"] = from_account
            data["UpdateItem"] = updateItems
            query = self._gen_query()
            return requests.post(rest_url, params=query, data=json.dumps(data))
        except Exception as e:
            logger.error("update freind failed:{}".format(e))
            return None

    def get_friends(self, from_account: str, start_index: int = 0):
        """
        get friends
        https://cloud.tencent.com/document/product/269/1647
        :param from_account
        :param:start_index: start index from next_start_index in response
        :return:response
        response.content
            {
            "UserDataItem": [
                {
                    "To_Account": "id1",
                    "ValueItem": [
                        {
                            "Tag": "Tag_SNS_IM_AddSource",
                            "Value": "AddSource_Type_Android"
                        },
                        {
                            "Tag": "Tag_SNS_IM_Remark",
                            "Value": "Remark1"
                        },
                        {
                            "Tag": "Tag_SNS_IM_Group",
                            "Value":["Group1","Group2"]
                        },
                        {
                            "Tag": "Tag_SNS_IM_AddTime",
                            "Value": 1563867420
                        },
                        {
                            "Tag": "Tag_SNS_Custom_Test",
                            "Value": "CustomData1"
                        }
                    ]
                },
                {
                    "To_Account": "id2",
                    "ValueItem": [
                        {
                            "Tag": "Tag_SNS_IM_AddSource",
                            "Value": "AddSource_Type_IOS"
                        },
                        {
                            "Tag": "Tag_SNS_IM_Group",
                            "Value":["Group1"]
                        },
                        {
                            "Tag": "Tag_SNS_IM_AddTime",
                            "Value": 1563867425
                        }
                    ]
                }
            ],
            "StandardSequence": 88,
            "CustomSequence": 46,
            "FriendNum": 20,
            "CompleteFlag": 1,
            "NextStartIndex": 0,
            "ActionStatus": "OK",
            "ErrorCode": 0,
            "ErrorInfo": "",
            "ErrorDisplay": ""
        }
        """

        rest_url = "{}/sns/friend_get".format(self.tecent_url)
        data = {}
        try:
            data["From_Account"] = from_account
            data["StartIndex"] = start_index
            query = self._gen_query()
            return requests.post(rest_url, params=query, data=json.dumps(data))
        except Exception as e:
            logger.error("get user failed:{}".format(e))
            return None

    def add_group(self, from_account: str, groups: List[str], to_accounts: List[str]):
        """
        add group
        https://cloud.tencent.com/document/product/269/10107
        :param from_account  :
        :param groups        ：list of groups
        :param to_accounts   ：add user id to groups
        :return:response
        response.content
        {
            "ResultItem":
            [
                {
                    "To_Account": "id1",
                    "ResultCode": 0,
                    "ResultInfo": ""
                },
                {
                    "To_Account": "id2",
                    "ResultCode": 32216,
                    "ResultInfo": "Err_SNS_GroupAdd_ToTinyId_Not_Friend"
                },
                {
                    "To_Account": "id3",
                    "ResultCode": 30002,
                    "ResultInfo": "ERR_SDKAPPID_ILLEGAL"
                }
            ],
            "Fail_Account":["id2","id3"],
            "CurrentSequence": 3,
            "ActionStatus": "OK",
            "ErrorCode": 0,
            "ErrorInfo": "",
            "ErrorDisplay": ""
        }

        """

        rest_url = "{}/sns/group_add".format(self.tecent_url)
        data = {}
        try:
            data["From_Account"] = from_account
            data["GroupName"] = groups
            data["To_Account"] = to_accounts
            query = self._gen_query()
            return requests.post(rest_url, params=query, data=json.dumps(data))
        except Exception as e:
            logger.error("add group failed:{}".format(e))
            return None

    def delete_group(self, from_account: str, groups: List[str]):
        """
        delete group
        https://cloud.tencent.com/document/product/269/10108
        :param: from_account:
        :param  groups: list of group names
        :return:response
        response.content
        {
            "CurrentSequence": 4,
            "ActionStatus":"OK",
            "ErrorCode":0,
            "ErrorInfo":"0",
            "ErrorDisplay":""
        }
        """
        try:
            rest_url = "{}/sns/group_delete".format(self.tecent_url)
            data = {}
            data["From_Account"] = from_account
            data["GroupName"] = groups
            query = self._gen_query()
            return requests.post(rest_url, params=query, data=json.dumps(data))

        except Exception as e:
            logger.error("delete group failed:{}".format(e))
            return None

    def get_group(
            self,
            from_account: str,
            groups: List[str] = [],
            need_friend_flag: str = "Need_Friend_Type_Yes"
    ):
        """
        get grounds
        https://cloud.tencent.com/document/product/269/54763
        :param from_account:
        :param: groups: list of group names
        :param: need_friend_flag: "Need_Friend_Type_Yes"
        :return: response
        response.content
        {
            "ResultItem": [
                {
                    "GroupName": "group1",
                    "FriendNumber": 1,
                    "To_Account": ["friend1"]
                }
            ],
            "CurrentSequence": 2,
            "ActionStatus": "OK",
            "ErrorCode": 0,
            "ErrorInfo": "",
            "ErrorDisplay": ""
        }

        """
        rest_url = "{}/sns/group_get".format(self.tecent_url)
        data = {}
        try:
            data["From_Account"] = from_account
            if len(groups) > 0:
                data["GroupName"] = groups
            data["NeedFriend"] = need_friend_flag
            query = self._gen_query()
            return requests.post(rest_url, params=query, data=json.dumps(data))
        except Exception as e:
            logger.error("get group failed:{}".format(e))
            return None

    def send_message(self,messgeObj:MessageObj):
        """
        send message
        https://cloud.tencent.com/document/product/269/2282
        :return: response
        response.content
        {
          "ActionStatus": "OK",
          "ErrorInfo": "",
          "ErrorCode": 0,
          "MsgTime": 1572870301,
          "MsgKey": "89541_2574206_1572870301"
        }
        """
        rest_url = "{}/openim/sendmsg".format(self.tecent_url)
        try:
            query = self._gen_query()
            return requests.post(rest_url, params=query, data=json.dumps(messgeObj.__dict__))
        except Exception as e:
            logger.error("send message faield:{}".format(e))
            return None

    def batch_send_message(self,batchMessageObj:BatchMessageObj):
      """
      batch send message
      https://cloud.tencent.com/document/product/269/2282
      :return: response
      response.content
        {
          "ActionStatus": "OK",
          "ErrorInfo": "",
          "ErrorCode": 0,
          "MsgTime": 1572870301,
          "MsgKey": "89541_2574206_1572870301"
        }
      """
      rest_url = "{}/openim/batchsendmsg".format(self.tecent_url)
      try:
        query = self._gen_query()
        return requests.post(rest_url, params=query, data=json.dumps(batchMessageObj.__dict__))
      except Exception as e:
        logger.error("batch send message faield:{}".format(e))
        return None

    def import_message_to_im(self,messgeObj:MessageObj,timestamp:int,sync_from_old:int=1):
        """
        import history message to im server
        https://cloud.tencent.com/document/product/269/2568
        :return: response
        response.content
        {
            "ActionStatus" : "OK",
            "ErrorInfo" : "",
            "ErrorCode" : 0
        }

        """
        rest_url = "{}/openim/importmsg".format(self.tecent_url)
        data = messgeObj.__dict__
        data["MsgTimeStamp"] = timestamp
        data["SyncFromOldSystem"] = sync_from_old

        try:
            query = self._gen_query()
            return requests.post(rest_url, params=query, data=json.dumps(data))
        except Exception as e:
            logger.error("import message failed:{}".format(e))
            return None

    def get_message_list(
            self,
            from_account:str,
            to_account:str,
            max_count:int,
            from_timestamp:int,
            to_timestamp:int,
            last_message_key:str=""):
        """
        get message
        https://cloud.tencent.com/document/product/269/42794
        :param from_account:
        :param to_account:
        :param max_count: number of messages
        :param from_timestamp: from timestamp
        :param to_timestamp:  from timestamp
        :param last_message_key: if you want get next message you should transfer it(from LastMsgKey)
        :return: response
        response.content
        {
            "ActionStatus": "OK",
            "ErrorInfo": "",
            "ErrorCode": 0,
            "Complete": 1,
            "MsgCnt": 1,
            "LastMsgTime": 1584669680,
            "LastMsgKey": "549396494_2578554_1584669680",
            "MsgList": [
                {
                    "From_Account": "user1",
                    "To_Account": "user2",
                    "MsgSeq": 549396494,
                    "MsgRandom": 2578554,
                    "MsgTimeStamp": 1584669680,
                    "MsgFlagBits": 0,
                    "MsgKey": "549396494_2578554_1584669680",
                    "MsgBody": [
                        {
                            "MsgType": "TIMTextElem",
                            "MsgContent": {
                                "Text": "1"
                            }
                        }
                    ],
                    "CloudCustomData": "your cloud custom data"
                }
            ]
        }
        """
        rest_url = "{}/openim/admin_getroammsg".format(self.tecent_url)
        data = {}
        data["From_Account"] = from_account
        data["To_Account"] = to_account
        data["MaxCnt"] = max_count
        data["MinTime"] = from_timestamp
        data["MaxTime"] = to_timestamp
        if last_message_key != "":
            data["LastMsgKey"] = last_message_key
        try:
            query = self._gen_query()
            return requests.post(rest_url, params=query, data=json.dumps(data))
        except Exception as e:
            logger.error("get message failed:{}".format(e))
            return None

    def draw_message(
            self,
            from_account:str,
            to_account:str,
            msg_key:str):
        """
        draw message
        https://cloud.tencent.com/document/product/269/38980

        :param from_account:
        :param to_account:
        :param msg_key:
        :return: resposne
        response.content
        {
            "ActionStatus": "OK",
            "ErrorInfo": "",
            "ErrorCode": 0
        }
        """
        rest_url = "{}/openim/admin_msgwithdraw".format(self.tecent_url)
        data = {}
        data["From_Account"] = from_account
        data["To_Account"] = to_account
        data["MsgKey"] = msg_key
        try:
            query = self._gen_query()
            return requests.post(rest_url, params=query, data=json.dumps(data))
        except Exception as e:
            logger.error("draw message failed:{}".format(e))
            return None

    def set_user_message_read(self,
                              from_account:str,
                              to_account:str,
                              read_timestamp:int=0):
        """
        set user message read
        https://cloud.tencent.com/document/product/269/50349
        :param from_account: user id for message read
        :param to_account:
        :param read_timestamp: read message before read_timestamp if message_read_timestamp we will set current time
        :return: response
        response.content
        {
            "ActionStatus": "OK",
            "ErrorInfo": "",
            "ErrorCode": 0
        }
        """
        rest_url = "{}/openim/admin_set_msg_read".format(self.tecent_url)
        data = {}
        data["Report_Account"] = from_account
        data["Peer_Account"] = to_account
        if read_timestamp != 0:
            data["MsgReadTime"] = read_timestamp
        try:
            query = self._gen_query()
            return requests.post(rest_url, params=query, data=json.dumps(data))
        except Exception as e:
            logger.error("set  message read failed:{}".format(e))
            return None

    def get_unread_num(self,from_account:str,to_accounts:List[str]=[]):
        """
        get unread message num
        https://cloud.tencent.com/document/product/269/56043
        :param from_account:
        :param to_accounts:
        :return: response
        response.content
        {
            "ActionStatus": "OK",
            "ErrorInfo": "",
            "ErrorCode": 0,
            "C2CUnreadMsgNumList": [
                {
                    "Peer_Account": "dramon2",
                    "C2CUnreadMsgNum": 12
                },
                {
                    "Peer_Account": "teacher",
                    "C2CUnreadMsgNum": 12
                }
            ]
        }
        """
        rest_url = "{}/openim/get_c2c_unread_msg_num".format(self.tecent_url)
        data = {}
        data["To_Account"] = from_account
        if len(to_accounts) >0:
            data["Peer_Account"] = to_accounts
        try:
            query = self._gen_query()
            return requests.post(rest_url, params=query, data=json.dumps(data))
        except Exception as e:
            logger.error("set  message read failed:{}".format(e))
            return None





if __name__ == "__main__":
    pass








