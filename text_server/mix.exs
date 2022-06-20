defmodule SampleApp.MixProject do
  use Mix.Project

  def project do
    [
      app: :sample_app,
      version: "0.1.0",
      elixir: "~> 1.9",
      start_permanent: Mix.env() == :prod,
      deps: deps()
    ]
  end

  # Run "mix help compile.app" to learn about applications.
  def application do
    [
      extra_applications: [:logger,:tesseract_ocr],
      mod: {SampleApp.Application, []}
    ]
  end

  # Run "mix help deps" to learn about dependencies.
  defp deps do
    [
      {:tesseract_ocr, "~> 0.1.5"},
      {:grpc, "~> 0.5.0-beta"},
      {:cowlib, "~> 2.8.0", hex: :grpc_cowlib, override: true}
    ]
  end
end
