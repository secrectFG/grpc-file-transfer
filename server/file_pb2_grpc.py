# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import file_pb2 as file__pb2


class FileStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.uploadSetName = channel.unary_unary(
                '/File/uploadSetName',
                request_serializer=file__pb2.FileSetNameReq.SerializeToString,
                response_deserializer=file__pb2.FileSetNameRsp.FromString,
                )
        self.upload = channel.stream_unary(
                '/File/upload',
                request_serializer=file__pb2.FileUploadReq.SerializeToString,
                response_deserializer=file__pb2.FileUploadRsp.FromString,
                )


class FileServicer(object):
    """Missing associated documentation comment in .proto file."""

    def uploadSetName(self, request, context):
        """rpc download(FileDownloadReq) returns (stream FileDownloadRsp) {}
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def upload(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_FileServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'uploadSetName': grpc.unary_unary_rpc_method_handler(
                    servicer.uploadSetName,
                    request_deserializer=file__pb2.FileSetNameReq.FromString,
                    response_serializer=file__pb2.FileSetNameRsp.SerializeToString,
            ),
            'upload': grpc.stream_unary_rpc_method_handler(
                    servicer.upload,
                    request_deserializer=file__pb2.FileUploadReq.FromString,
                    response_serializer=file__pb2.FileUploadRsp.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'File', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class File(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def uploadSetName(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/File/uploadSetName',
            file__pb2.FileSetNameReq.SerializeToString,
            file__pb2.FileSetNameRsp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def upload(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_unary(request_iterator, target, '/File/upload',
            file__pb2.FileUploadReq.SerializeToString,
            file__pb2.FileUploadRsp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
