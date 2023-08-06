import json
import math
import os

from intelliw.config import config
from intelliw.datasets.datasource_base import AbstractDataSource, DataSourceReaderException
from intelliw.utils import iuap_request
from intelliw.utils.logger import get_logger

logger = get_logger()


def err_handler(request, exception):
    print("请求出错,{}".format(exception))


class DataSourceIwImgData(AbstractDataSource):
    """
    非结构化存储数据源
    图片数据源
    """

    def __init__(self, input_address, get_row_address, ds_id, ds_type):
        """
        智能分析数据源
        :param input_address:   获取数据 url
        :param get_row_address: 获取数据总条数 url
        :param ds_id:   数据集Id
        """
        self.input_address = input_address
        self.get_row_address = get_row_address
        self.ds_id = ds_id
        self.ds_type = ds_type

    def total(self):
        params = {'dsId': self.ds_id, 'yTenantId': config.TENANT_ID}
        response = iuap_request.get(self.get_row_address, params=params)
        if 200 != response.status:
            msg = "获取行数失败，url: {}, response: {}".format(
                self.get_row_address, response)
            logger.error(msg)
            raise DataSourceReaderException(msg)

        row_data_str = response.body
        row_data = json.loads(row_data_str)
        data_num = row_data['data']

        if not isinstance(data_num, int):
            msg = "获取行数返回结果错误, response: {}, request_url: {}".format(
                row_data_str, self.get_row_address)
            logger.error(msg)
            raise DataSourceReaderException(msg)

        return data_num

    def reader(self, page_size=1000, offset=0, limit=0, transform_function=None):
        return self.__Reader(self.input_address, self.ds_id, self.ds_type, self.total(), page_size, offset, limit, transform_function)

    class __Reader:
        def __init__(self, input_address, ds_id, ds_type, total, page_size=100, offset=0, limit=0, transform_function=None):
            """
            eg. 91 elements, page_size = 20, 5 pages as below:
            [0,19][20,39][40,59][60,79][80,90]
            offset 15, limit 30:
            [15,19][20,39][40,44]
            offset 10 limit 5:
            [10,14]
            """
            if offset > total:
                msg = "偏移量大于总条数:偏移 {}, 总条数: {}".format(offset, total)
                logger.error(msg)
                raise DataSourceReaderException(msg)
            self.input_address = input_address
            self.ds_id = ds_id
            self.ds_type = ds_type
            self.limit = limit
            self.offset = offset
            self.total = total
            if limit <= 0:
                self.limit = total - offset
            elif offset + limit > total:
                self.limit = total - offset
            self.page_size = page_size
            self.total_page = math.ceil(total / self.page_size)
            self.start_page = math.floor(offset / self.page_size)
            self.end_page = math.ceil((offset + self.limit) / page_size) - 1
            self.start_index_in_start_page = offset - self.start_page * page_size
            self.end_index_in_end_page = offset + self.limit - 1 - self.end_page * page_size
            self.current_page = self.start_page

            self.transform_function = transform_function
            self.total_read = 0
            self.after_transform = 0
            """
            print("total_page={},start_page={},end_page={},start_index={},end_index={},current_page={}"
                  .format(self.total_page,
                          self.start_page,
                          self.end_page,
                          self.start_index_in_start_page,
                          self.end_index_in_end_page,
                          self.current_page))
            """

        @property
        def iterable(self):
            return True

        def __iter__(self):
            return self

        def __next__(self):
            if self.current_page > self.end_page:
                logger.info('共读取原始数据 {} 条，经特征工程处理后数据有 {} 条'.format(
                    self.total_read, self.after_transform))
                raise StopIteration

            try:
                page = self._read_page(self.current_page, self.page_size)

                if self.current_page == self.start_page or self.current_page == self.end_page:
                    # 首尾页需截取有效内容
                    start_index = 0
                    end_index = len(page['data']['content']) - 1
                    if self.current_page == self.start_page:
                        start_index = self.start_index_in_start_page
                    if self.current_page == self.end_page:
                        end_index = self.end_index_in_end_page
                    # print("start_index={},end_index={}".format(start_index, end_index))
                    page['data']['content'] = page['data']['content'][start_index: end_index + 1]

                data = self._download(page)

                self.current_page += 1
                self.total_read += len(page['data']['content'])
                if self.transform_function is not None:
                    transformed = self.transform_function(data)
                    self.after_transform += len(transformed)
                    return transformed
                self.after_transform = self.total_read
                return data
            except Exception as e:
                logger.exception(
                    "智能分析数据源读取失败, input_address: [{}]".format(self.ds_id))
                raise DataSourceReaderException('智能分析数据源读取失败') from e

        def _read_page(self, page_index, page_size):
            """
            调用智能分析接口，分页读取数据
            :param page_index: 页码，从 0 开始
            :param page_size:  每页大小
            :return:
            """
            request_data = {'dsId': self.ds_id, 'pageNumber': page_index,
                            'pageSize': page_size, 'yTenantId': config.TENANT_ID,
                            'type': self.ds_type}
            response = iuap_request.get(
                url=self.input_address, params=request_data)
            response.raise_for_status()
            return json.loads(response.body)

        def _download(self, page) -> list:
            """
            调用对象存储服务url下载图片和标注信息
            Args:
                page:
            Returns:[[图片,标注],[图片,标注]]
            """
            urls = []
            annotation_urls = []
            files = []
            annotations = []
            data = []
            for file in page['data']['content']:
                urls.append(file['url'])
                annotation_urls.append(file['annotationUrl'])
            from concurrent.futures import ThreadPoolExecutor as PoolExecutor
            with PoolExecutor(max_workers=os.cpu_count() * 2) as executor:
                for file in executor.map(do_http_get, urls):
                    files.append(file)
            with PoolExecutor(max_workers=os.cpu_count() * 2) as executor:
                for annotation in executor.map(do_http_get, annotation_urls):
                    annotations.append(annotation)

            for i in range(len(urls)):
                if files[i] is not None and annotations[i] is not None:
                    row = [files[i], annotations[i]]
                    data.append(row)
            return data


def do_http_get(url):
    import requests
    requests.packages.urllib3.disable_warnings()
    try:
        response = requests.get(url, verify=False)
        status = response.status_code
        if status == 200:
            return response.content
        else:
            logger.error(
                "http get url {} failed, status is {}".format(url, status))
            return None
    except requests.HTTPError as e:
        logger.error("http get url {} failed, error is {}".format(url, e))
        return None
