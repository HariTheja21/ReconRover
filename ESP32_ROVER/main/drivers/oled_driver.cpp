#include "oled_driver.h"

namespace ReconRover {
namespace Drivers {

OLEDDriver::OLEDDriver(DriverStatistics& stats) : stats_(stats) {}

void OLEDDriver::Init() {
    // Initialize I2C Master, configure SSD1306/SH1106
}

void OLEDDriver::SetDisplayMode(uint8_t mode) {
    // Hardware abstraction:
    // switch (mode) {
    //   case 0: display.clear(); display.drawString("IDLE"); break;
    //   case 1: display.clear(); display.drawString("DRIVING"); break;
    //   case 99: display.clear(); display.drawString("E-STOP"); break;
    // }
    // display.display();

    stats_.oled_updates++;
}

} // namespace Drivers
} // namespace ReconRover
