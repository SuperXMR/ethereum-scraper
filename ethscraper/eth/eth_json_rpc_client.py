import scrapy
import json

from ethscraper.utils import generate_get_block_by_number_json_rpc


class EthJsonRpcClient(object):
    def __init__(self, url):
        if not url:
            raise ValueError('url can\'t be None or empty')
        self.url = url

    def eth_getBlockByNumber(self, block=0, tx_objects=True):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_getblockbynumber
        """
        block = self.validate_block(block)
        return self._call('eth_getBlockByNumber', [block, tx_objects])

    def eth_getBlockByNumberBatch(self, start, end, tx_objects=True):
        return self._call_batch(start, end, tx_objects)

    def eth_getTransactionReceipt(self, tx_hash):
        """
        https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_gettransactionreceipt
        """
        return self._call('eth_getTransactionReceipt', [tx_hash])

    def _call(self, method, params=None, _id=1):
        data = {
            'jsonrpc': '2.0',
            'method': method,
            'params': params,
            'id': _id,
        }
        return scrapy.Request(self.url,
                              method='POST',
                              body=json.dumps(data),
                              headers={'Content-Type': 'application/json'})

    def _call_batch(self, start, end, include_transactions):
        blocks_rpc = list(generate_get_block_by_number_json_rpc(start, end, include_transactions))

        return scrapy.Request(self.url,
                              method='POST',
                              body=json.dumps(blocks_rpc),
                              headers={'Content-Type': 'application/json'})

    @staticmethod
    def validate_block(block):
        if isinstance(block, int):
            block = hex(block)
        return block
