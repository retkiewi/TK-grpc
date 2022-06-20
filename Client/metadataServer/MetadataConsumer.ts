// create a rabbitmq queue consumer

import handleRequest, { filterMetadata } from '../MetadataFilter/metadata'
import MetadataOptions from '../MetadataFilter/metadataOptions.interface'
import fs from 'fs';
import ini from 'ini';
import MetadataRequest from '../MetadataFilter/metadataRequest';

const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');

const read_ini_file = (file_name: string): any => {
    return ini.parse(fs.readFileSync(file_name, 'utf-8'))
}

const {GRPC: {metadata: address}} = read_ini_file("Client/config.ini")

const PROTO_PATH = __dirname + '/../protos/core-metadata.proto';

const packageDefinition = protoLoader.loadSync(
    PROTO_PATH,
    {keepCase: true,
     longs: String,
     enums: String,
     defaults: true,
     oneofs: true
    });

let metadata_proto = grpc.loadPackageDefinition(packageDefinition).metadata;

const server = new grpc.Server();

const getResult = (call: any, callback: any) => {
    const request = call.request;
    console.log('Received request:');
    console.log(request)
    filterMetadata(request.path, request as MetadataOptions).then(result => {
        console.log(result);
        callback(null, {return_value: result});
    });
}

// @ts-ignore
server.addService(metadata_proto.Metadata.service, {get_result: getResult});

server.bindAsync(address, grpc.ServerCredentials.createInsecure(), () => {
    server.start();
    console.log('Server started :)')
  });
