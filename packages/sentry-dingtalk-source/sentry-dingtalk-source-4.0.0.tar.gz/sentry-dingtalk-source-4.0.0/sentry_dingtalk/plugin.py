"""
  @Project     : sentry-dingtalk
  @Time        : 2022/04/15 15:35:12
  @File        : plugin.py
  @Author      : source
  @Software    : VSCode
  @Desc        :
"""


import requests
import six
import ast
from sentry import tagstore
from sentry.plugins.bases import notify
from sentry.utils import json
from sentry.utils.http import absolute_uri
from sentry.integrations import FeatureDescription, IntegrationFeatures
from sentry_plugins.base import CorePluginMixin
from django.conf import settings


class DingTalkPlugin(CorePluginMixin, notify.NotificationPlugin):
    title = "DingTalk"
    slug = "dingtalk"
    description = "Post notifications to Dingtalk."
    conf_key = "dingtalk"
    required_field = "webhook"
    author = "source"
    author_url = "https://gitlab.xiaoman.cc/sourceliu/sentry-dingtalk-source"
    version = "4.0.0"
    resource_links = [
        ("Report Issue", "https://gitlab.xiaoman.cc/sourceliu/sentry-dingtalk-source/issues"),
        ("View Source", "https://gitlab.xiaoman.cc/sourceliu/sentry-dingtalk-source"),
    ]

    feature_descriptions = [
        FeatureDescription(
            """
                Configure rule based Dingtalk notifications to automatically be posted into a
                specific channel.
                """,
            IntegrationFeatures.ALERT_RULE,
        )
    ]

    def is_configured(self, project):
        return bool(self.get_option("webhook", project))

    def get_config(self, project, **kwargs):
        return [
            {
                "name": "webhook",
                "label": "webhook",
                "type": "url",
                "placeholder": "https://oapi.dingtalk.com/robot/send?access_token=**********",
                "required": True,
                "help": "钉钉 webhook 会@ 成员",
                "default": self.set_default(project, "webhook", "DINGTALK_WEBHOOK"),
            },
            {
                "name": "webhook_optional",
                "label": "webhook_optional",
                "type": "url",
                "placeholder": "{项目:钉钉用户id}",
                "required": True,
                "help": "项目对应负责人",
                "default": self.set_default(
                    project, "webhook_optional", ""
                ),
            },
            {
                "name": "ats",
                "label": "@成员",
                "type": "string",
                "placeholder": "默认通知的钉钉用户ID",
                "required": False,
                "help": "项目无对应人员时@的用户,逗号分隔多个",
                "default": self.set_default(
                    project, "ats", ""
                ),
            },
        ]

    def set_default(self, project, option, env_var):
        if self.get_option(option, project) != None:
            return self.get_option(option, project)
        if hasattr(settings, env_var):
            return six.text_type(getattr(settings, env_var))
        return None

    def notify(self, notification, raise_exception=False):
        event = notification.event
        user = event.get_minimal_user()
        user_id = user.id
        release = event.release
        group = event.group
        project = group.project
        self._post(group, user_id, release, project)

    def _post(self, group, userId, release, project):
        webhook = self.get_option("webhook", project)
        # 项目负责人
        webhook_optional = self.get_option("webhook_optional", project)
        lite = ast.literal_eval(webhook_optional)
        project_user = None
        # 如果项目负责人存在
        if project.name in lite:
            project_user = lite[project.name].split(",")
       
        # 默认艾特的用户
        ats_str = self.get_option("ats", project)
        if ats_str == None:
            ats_str = ""
        ats_array = ats_str.split(",")

        # 如果项目负责人不存在 艾特默认负责人
        if project_user == None:
            project_user = ats_array

        ats_ding_str = ""
        for at in project_user:
            ats_ding_str = f"{ats_ding_str} @{at} "
            

        issue_link = group.get_absolute_url(params={"referrer": "dingtalk"})

        payload = f"### 「⚠️ 前端监控告警」\n\n"
        payload = f"{payload} #### 项目名：{project.name}\n\n"
        payload = f"{payload} #### 项目跟进人：{ats_ding_str}\n\n"
        payload = f"{payload} #### 版本：{release} \n\n"
        payload = f"{payload} #### 异常信息：> {group.message}\n >[查看错误日志]({issue_link}) \n\n"
        payload = f"{payload} ###### 请项目负责人及时查看分配处理[客服]\n\n"

        headers = {
            "Content-type": "application/json",
            "Accept": "text/plain",
            "charset": "utf8"
        }

        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": "⚠️ 前端监控告警",
                "text": payload,
            },
            "at": {
                "atUserIds": project_user,
                "isAtAll": "false"
            }
        }
        requests.post(webhook, data=json.dumps(data), headers=headers)
