#include <stdio.h>
#include <EDSDK.h>

int main() {
    if (EDS_Init() == 0) {
        printf("EDS_Init succeeded\n");
    } else {
        printf("EDS_Init failed\n");
    }
    return 0;
}
