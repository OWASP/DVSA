resource azurerm_app_service "app-service2" {
  app_service_plan_id = azurerm_app_service_plan.example.id
  location            = var.location
  name                = "terragoat-app-service-${var.environment}${random_integer.rnd_int.result}"
  resource_group_name = azurerm_resource_group.example.name
  https_only          = true

  auth_settings {
    enabled = true
  }
  client_cert_enabled = true
  site_config {
    dotnet_framework_version = "v5.0"
    ftps_state = "Disabled"
    http2_enabled = true
  }
  logs {
    detailed_error_messages_enabled = true
    failed_request_tracing_enabled = true
  }
  storage_account {
    type = "AzureFiles"
  }
}
