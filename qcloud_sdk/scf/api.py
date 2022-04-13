# -*- coding: utf-8 -*-


class ScfAPIMixin(object):
    def request_scf_api(self, action, params):
        return self.request_api(service='scf', action=action, params=params, api_version='2018-04-16')

    # ----- 函数API -----
    # --- 函数运行API ---
    def invoke_function(self):
        """

        https://cloud.tencent.com/document/product/583/17243

        :return:
        """
        return self.request_scf_api(action='Invoke', params={})

    def update_function_code(self):
        """
        https://cloud.tencent.com/document/product/583/18581

        :return:
        """
        return self.request_scf_api(action='UpdateFunctionCode', params={})

    # --- 函数资源管理API ---
    def list_functions(self):
        """

        https://cloud.tencent.com/document/product/583/18582

        :return:
        """
        return self.request_scf_api(action='ListFunctions', params={})

    def get_function(self):
        """

        https://cloud.tencent.com/document/product/583/18584

        :return:
        """
        return self.request_scf_api(action='GetFunction', params={})

    def create_function(self):
        """

        https://cloud.tencent.com/document/product/583/17243

        :return:
        """
        return self.request_scf_api(action='CreateFunction', params={})

    def delete_function(self):
        """

        https://cloud.tencent.com/document/product/583/18585

        :return:
        """
        return self.request_scf_api(action='DeleteFunction', params={})

    def recreate_function(self):
        """
        (high-level API) 重新创建函数
          - 如果已经存在，则销毁以后重建；
          - 如果不存在，则直接重建。
        :return:
        """
        if self.get_function():
            self.delete_function()
        self.create_function()

    # ----- 触发器API -----
    def create_trigger(self):
        """

        https://cloud.tencent.com/document/product/583/18589

        :return:
        """
        pass

    def delete_trigger(self):
        """
        https://cloud.tencent.com/document/product/583/18588
        :return:
        """
        pass

    def list_triggers(self):
        """
        https://cloud.tencent.com/document/product/583/44268
        :return:
        """
        pass
