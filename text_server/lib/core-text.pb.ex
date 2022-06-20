defmodule TextRequest do
  @moduledoc false
  use Protobuf, protoc_gen_elixir_version: "0.10.0", syntax: :proto3

  field :image_path, 1, type: :string, json_name: "imagePath"
  field :hasText, 2, type: :bool
  field :containsText, 3, type: :string
  field :minLength, 4, type: :int32
  field :maxLength, 5, type: :int32
end
defmodule TextReply do
  @moduledoc false
  use Protobuf, protoc_gen_elixir_version: "0.10.0", syntax: :proto3

  field :return_value, 1, type: :bool, json_name: "returnValue"
end
defmodule Text.Service do
  @moduledoc false
  use GRPC.Service, name: "Text", protoc_gen_elixir_version: "0.10.0"

  rpc :get_result, TextRequest, TextReply
end

defmodule Text.Stub do
  @moduledoc false
  use GRPC.Stub, service: Text.Service
end
