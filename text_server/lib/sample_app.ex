defmodule SampleApp.User.Server do
  use GRPC.Server, service: Text.Service

  def get_result(request, _stream) do
    IO.inspect(request)

    options = Map.new()

    options =
      if request.hasText == true do
        Map.put(options, "hasText", "true")
      else
        options
      end

    options =
      if String.length(request.containsText) > 0 do
        Map.put(options, "containsText", request.containsText)
      else
        options
      end

    options =
      if request.minLength > 0 do
        Map.put(options, "minLength", request.minLength)
      else
        options
      end

    options =
      if request.maxLength > 0 do
        Map.put(options, "maxLength", request.maxLength)
      else
        options
      end

    options =
      if request.hasText == false do
        Map.put(options, "hasText", "false")
      else
        options
      end

    IO.inspect(options)
    ocr_result = Ocr.checkImage(request.image_path, options)

    response = %{
      return_value: ocr_result
    }

    IO.inspect(response)
    TextReply.new(response)
  end
end
