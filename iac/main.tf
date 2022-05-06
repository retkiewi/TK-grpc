resource "azurerm_resource_group" "cognitive-rg" {
    name     = "cognitive-rg-tk"
    location = var.default_location
}

resource "azurerm_cognitive_account" "tk-style-comp" {
    name                = "tk-style-comp"
    location            = var.default_location
    resource_group_name = azurerm_resource_group.cognitive-rg.name
    kind                = "ComputerVision"
  
    sku_name = "F0"
}
