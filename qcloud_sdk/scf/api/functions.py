# -*- coding: utf-8 -*-


class ScfFunctionAPIMixin(object):
    """
    函数相关API
    """
    # ----- 函数执行API -----
    def invoke_function(self, function_name, region=None, **kwargs):
        """
        执行函数

        https://cloud.tencent.com/document/product/583/17243

        TODO：
          - 增加可选参数。

        :return:
        """
        params = {
            'FunctionName': function_name,
        }
        return self.request_scf_api(action='Invoke', params=params, region=region)['Result']

    # ----- 函数配置API -----
    def update_function_code(self):
        """
        https://cloud.tencent.com/document/product/583/18581

        :return:
        """
        return self.request_scf_api(action='UpdateFunctionCode', params={})

    # ----- 函数资源管理API -----
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


class ScfFunctionIntegratedAPIMixin(object):
    # ----- 函数执行API -----
    def retry_invoke_function(self):
        pass

    # ----- 函数资源管理API -----
    def has_function(self):
        return bool(self.get_function())

    def create_or_update_function(self):
        pass

    def recreate_function(self):
        """
        重新创建函数
          - 如果已经存在，则销毁以后重建；
          - 如果不存在，则直接重建。
        :return:
        """
        if self.has_function():
            self.delete_function()
        self.create_function()
