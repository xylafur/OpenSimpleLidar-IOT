deps_config := \
	/home/yelsek/esp/esp-idf/components/app_trace/Kconfig \
	/home/yelsek/esp/esp-idf/components/aws_iot/Kconfig \
	/home/yelsek/esp/esp-idf/components/bt/Kconfig \
	/home/yelsek/esp/esp-idf/components/driver/Kconfig \
	/home/yelsek/esp/esp-idf/components/efuse/Kconfig \
	/home/yelsek/esp/esp-idf/components/esp32/Kconfig \
	/home/yelsek/esp/esp-idf/components/esp_adc_cal/Kconfig \
	/home/yelsek/esp/esp-idf/components/esp_event/Kconfig \
	/home/yelsek/esp/esp-idf/components/esp_http_client/Kconfig \
	/home/yelsek/esp/esp-idf/components/esp_http_server/Kconfig \
	/home/yelsek/esp/esp-idf/components/esp_https_ota/Kconfig \
	/home/yelsek/esp/esp-idf/components/espcoredump/Kconfig \
	/home/yelsek/esp/esp-idf/components/ethernet/Kconfig \
	/home/yelsek/esp/esp-idf/components/fatfs/Kconfig \
	/home/yelsek/esp/esp-idf/components/freemodbus/Kconfig \
	/home/yelsek/esp/esp-idf/components/freertos/Kconfig \
	/home/yelsek/esp/esp-idf/components/heap/Kconfig \
	/home/yelsek/esp/esp-idf/components/libsodium/Kconfig \
	/home/yelsek/esp/esp-idf/components/log/Kconfig \
	/home/yelsek/esp/esp-idf/components/lwip/Kconfig \
	/home/yelsek/esp/esp-idf/components/mbedtls/Kconfig \
	/home/yelsek/esp/esp-idf/components/mdns/Kconfig \
	/home/yelsek/esp/esp-idf/components/mqtt/Kconfig \
	/home/yelsek/esp/esp-idf/components/nvs_flash/Kconfig \
	/home/yelsek/esp/esp-idf/components/openssl/Kconfig \
	/home/yelsek/esp/esp-idf/components/pthread/Kconfig \
	/home/yelsek/esp/esp-idf/components/spi_flash/Kconfig \
	/home/yelsek/esp/esp-idf/components/spiffs/Kconfig \
	/home/yelsek/esp/esp-idf/components/tcpip_adapter/Kconfig \
	/home/yelsek/esp/esp-idf/components/unity/Kconfig \
	/home/yelsek/esp/esp-idf/components/vfs/Kconfig \
	/home/yelsek/esp/esp-idf/components/wear_levelling/Kconfig \
	/home/yelsek/esp/esp-idf/components/wifi_provisioning/Kconfig \
	/home/yelsek/esp/esp-idf/components/app_update/Kconfig.projbuild \
	/home/yelsek/esp/esp-idf/components/bootloader/Kconfig.projbuild \
	/home/yelsek/esp/esp-idf/components/esptool_py/Kconfig.projbuild \
	/home/yelsek/esp/tcp_server/main/Kconfig.projbuild \
	/home/yelsek/esp/esp-idf/components/partition_table/Kconfig.projbuild \
	/home/yelsek/esp/esp-idf/Kconfig

include/config/auto.conf: \
	$(deps_config)

ifneq "$(IDF_TARGET)" "esp32"
include/config/auto.conf: FORCE
endif
ifneq "$(IDF_CMAKE)" "n"
include/config/auto.conf: FORCE
endif

$(deps_config): ;
