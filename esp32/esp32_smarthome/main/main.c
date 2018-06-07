#include <string.h>
#include <sys/socket.h>

#include "freertos/FreeRTOS.h"

int app_main(void)
{
    while (1)
    {
        vTaskDelay(1000);
        printf("Hello");
        fflush(stdout);
    }
    return 0;
}
