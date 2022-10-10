/*******************************************************************************
* File Name: main.c
*
* Version: 1.10
*
* Description:
*  This is source code for forwarding data to and from the Raspberry Pi through the Cyprus, and monitoring battery connection.
*  Parameters used:
*   Mode                CPHA == 0, CPOL == 0                
*   Data lines          MOSI+MISO
*   Shift direction     MSB First
*   DataBits:           8 
*   Bit Rate            1 Mbps
*   Clock source        External  
*
********************************************************************************
* Copyright 2012-2015, Cypress Semiconductor Corporation. All rights reserved.
* This software is owned by Cypress Semiconductor Corporation and is protected
* by and subject to worldwide patent and copyright laws and treaties.
* Therefore, you may use this software only as provided in the license agreement
* accompanying the software package from which you obtained this software.
* CYPRESS AND ITS SUPPLIERS MAKE NO WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
* WITH REGARD TO THIS SOFTWARE, INCLUDING, BUT NOT LIMITED TO, NONINFRINGEMENT,
* IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
*******************************************************************************/
#include <project.h>

#define COMMAND_MASK 0xFF00
#define PORT_MASK 0x00F0
#define PARAMETER_MASK 0x00F0
#define CHANNEL_MASK 0x000F
#define DATA_MASK 0x00F0
#define READ_ENCODER 0x10
#define ENCODER_IDLE 0xA5
#define ORDINAL_MASK 0x000F
#define TRIGGER_OFF 0xFFFF
#define TRIGGER_RESET_MASK 0x00F0
#define DEFAULT_TRIGGER_RADIUS 0x5
#define GPIO_MODE 0x0 
#define TRIGGER_MODE 0x1
#define NOT_READY 0x0000
#define READY 0xFFFF
#define TRUE 0x1
#define FALSE 0x0

typedef enum { 
    NA, 
    ready, 
    not_ready 
} readiness_state; 
 
typedef enum { 
    idle_state, 
    listening_state, 
    execution_state, 
    responding_state 
} state;

typedef enum {
    no_command,
    read_gpio,
    write_gpio,
    read_spi,
    write_spi,
    write_pwm,
    read_i2c,
    write_i2c,
    add_i2c_data,
    add_i2c_address,
    set_spi_trigger,
    read_encoder,
    set_trigger_radius,
    set_pinmode,
    read_firmware_date
} command;

uint16 ReadWriteSPIM1(uint8, uint8);
uint16 ReadWriteSPIM2(uint8, uint16);
uint16 ReadEncoder(uint8, uint8);
command InterpretCommand(uint16);
int abs(int);

uint16 RPi_Command_Data;
uint16 RPi_Data;
state PSOC_state;
command RPi_Command;
uint16 shutdown_count;
uint8 i2c_data_to_write[8];
uint8 i2c_address = 0;
uint8 i2c_byte_count = 0;
uint16 spi_trigger_value[4] = {TRIGGER_OFF, TRIGGER_OFF, TRIGGER_OFF, TRIGGER_OFF};
uint8  spi_trigger_reset[4] = {FALSE, FALSE, FALSE, FALSE};
uint16 spi_trigger_radius[4] = {DEFAULT_TRIGGER_RADIUS, DEFAULT_TRIGGER_RADIUS, DEFAULT_TRIGGER_RADIUS, DEFAULT_TRIGGER_RADIUS};
uint8  spi_trigger_hit[4] = {FALSE, FALSE, FALSE, FALSE};
uint8 pinmode = TRIGGER_MODE;
readiness_state readiness = not_ready; 
uint16 response_value = 0x0;

uint8_t firmwareVersionDate[] = {3, 1, 2, 11, 29, 19};

CY_ISR(SS_Rise_Handler) { 
    if (PSOC_state == idle_state) { 
        RPi_Command_Data = SPIS_ReadRxData(); 
        RPi_Command = InterpretCommand(RPi_Command_Data); 
        SPIS_ClearRxBuffer(); 
        if((RPi_Command == write_gpio) ||  
           (RPi_Command == write_spi) ||  
           (RPi_Command == write_pwm) ||  
           (RPi_Command == read_i2c) || 
           (RPi_Command == add_i2c_data) ||  
           (RPi_Command == add_i2c_address) ||  
           (RPi_Command == set_spi_trigger) || 
           (RPi_Command == set_trigger_radius) || 
           (RPi_Command == set_pinmode)) { 
            PSOC_state = listening_state; 
        } else { 
            PSOC_state = execution_state; 
        } 
 
        if ((RPi_Command == read_gpio) || 
            (RPi_Command == read_spi) || 
            (RPi_Command == read_i2c) || 
            (RPi_Command == read_encoder) || 
            (RPi_Command == read_firmware_date)) { 
            readiness = not_ready;
        } else { 
            readiness = NA; 
        }

        SPIS_WriteTxDataZero(NOT_READY); 
    } else if (PSOC_state == listening_state) { 
        RPi_Data = SPIS_ReadRxData(); 
        PSOC_state = execution_state; 
        SPIS_ClearRxBuffer(); 
    } else if (PSOC_state == execution_state) { 
        if (readiness == not_ready) { 
            SPIS_WriteTxDataZero(NOT_READY); 
        } else if (readiness == ready) { 
            PSOC_state = responding_state; 
            SPIS_WriteTxDataZero(response_value); 
        } 
    } else if (PSOC_state == responding_state) { 
        PSOC_state = idle_state; 
    } 
     
    SPIS_ReadRxStatus(); 
    SPIS_ClearRxBuffer(); 
    isr_SS_Rise_ClearPending(); 
} 

/* The txBuffer size is equal (BUFFER_SIZE-1) because for SPI Mode where CPHA == 0 and
* CPOL == 0 one byte writes directly in SPI TX FIFO using SPIS_WriteTxDataZero() API.
*/
uint8 isRPiCommand(command rpiCommand) {
    switch (rpiCommand) {
        case read_gpio:
        case write_gpio:
        case read_spi:
        case write_spi:
        case write_pwm:
        case read_i2c:
        case write_i2c:
        case read_encoder:
        case add_i2c_data:
        case add_i2c_address:
        case set_spi_trigger:
        case set_trigger_radius:
        case set_pinmode:
        case read_firmware_date:
            return 1;
            break;
        
        case no_command:
        default:
            return 0;
            break;
    }

    return 0;
}

/*Command Structure: 0x0CPQ --> execute command C with parameters P and Q
 *Some commands take no parameters, and are of the form 0x0C00
 */
command InterpretCommand(uint16 data)
{
    command result = no_command;
    uint16 cmd = (data & COMMAND_MASK);
    
    switch(cmd) {  
        case 0x0100:
            result = read_gpio;
            break;
        case 0x0200:
            result = write_gpio;
            break;        
        case 0x0300:
            result = read_spi;
            break;        
        case 0x0400:
            result = write_spi;
            break;        
        case 0x0500:
            result = write_pwm;
            break;        
        case 0x0600:
            result = read_i2c;
            break;        
        case 0x0700:
            result = write_i2c;
            break;        
        case 0x0800:
            result = add_i2c_data;
            break;        
        case 0x0900:
            result = add_i2c_address;
            break;        
        case 0x0a00:
            result = set_spi_trigger;
            break;
        case 0x0b00:
            result = read_encoder;
            break;
        case 0x0c00:
            result = set_trigger_radius;
            break;
        case 0x0d00: 
            result = set_pinmode; 
            break;
        case 0x0f00:
            result = read_firmware_date;
            break;
        default:
            result = no_command;
            break;
    }
    
    return result;
}

int main() {
    RpiInterrupts_Write(3u);  // 9.25.18 - New location, trying to force the interrupts high as early as possible
    Comp_1_Start();
    CyDelay(2000u);
    
    /* Enable Battery Backup circuit and interface circuits between RPi and PSOC  */
    EnableBattery_Write(1u);
    Control_Reg_SS_1_Write(0u);
    
    //RpiInterrupts_Write(3u);     // 9.25.18 - Original location, moving this to the start of this function
    Clock_1_Start();
 
    SPIM_1_Start();
    SPIM_1_ClearFIFO();
    SPIM_1_ClearRxBuffer();
    SPIM_1_ClearTxBuffer();   
    
    SPIM_2_Start();
    SPIM_2_ClearFIFO();
    SPIM_2_ClearRxBuffer();
    SPIM_2_ClearTxBuffer();    

    SPIS_Start();
    SPIS_WriteTxDataZero(0x00u);
 
    PWM_1_Start();
    PWM_2_Start();
    PWM_1_SetCompareMode(PWM_1__B_PWM__LESS_THAN);
    PWM_2_SetCompareMode(PWM_1__B_PWM__LESS_THAN);
    
    I2C_1_Start();   
    
    PSOC_state = idle_state;
      
    CyGlobalIntEnable; 
    isr_SS_Rise_StartEx( SS_Rise_Handler );
 
    RPi_Command_Data = 0x000f;
    shutdown_count = 0;

    while (1)  { 
        // This code monitors the main power input.  A local backup batter supply prevents
        // power from being removed from the raspberry pi before it has been properly shutdown
        // Monitor the presence of the main power input. If power has been removed for more 
        // than 5000 times through this loop (about 20 seconds), interrupt the Raspberry Pi 
        // telling it to shut itself down allow 20 sec for the Pi to shut down then turn off 
        // back up power.
        CyDelayUs(1400u);   
        if (Status_Reg_1_Read() == 1u) {
            shutdown_count +=1;
            if (shutdown_count == 2000u) {   //9.25.18 - The while loop executes in about 2ms total.
                                             //          2ms * 2000 = 4 seconds, not 20 seconds as described above.
                                             //          Changing to 10000 to get 20 seconds.      
                CyGlobalIntDisable; 
                
                // tell Pi to shut down
                RpiInterrupts_Write(0u);
                CyDelay(20000u);
                
                // Wait 60 seconds then turn off back up power
                EnableBattery_Write(2u);
                CyDelay(2000u);
            }
        } else {
           shutdown_count = 0u;
        }
    
        // Writes corresponding GPIO high if encoder value is within specified range of trigger value
        if (pinmode == TRIGGER_MODE) { 
            for (int i = 0; i < 4; i++) { 
                int encoderValue; 
             
                if (i == 3) {
                    encoderValue = ReadEncoder(2, 0); 
                } else { 
                    encoderValue = ReadEncoder(1, i); 
                }
 
                if (abs(encoderValue - spi_trigger_value[i]) < spi_trigger_radius[i]) {
                    if (spi_trigger_hit[i] == FALSE) {
                        GPIO_Control_Reg_Write(GPIO_Status_Reg_Read() | (1 << i));
                        spi_trigger_hit[i] = TRUE;
                        if (spi_trigger_reset[i] == TRUE) { 
                            spi_trigger_reset[i] = FALSE; 
                            spi_trigger_value[i] = TRIGGER_OFF; 
                        }
                    } else {
                        GPIO_Control_Reg_Write(GPIO_Status_Reg_Read() & (0xF-(1 << i)));
                    }
                } else { 
                    GPIO_Control_Reg_Write(GPIO_Status_Reg_Read() & (0xF-(1 << i)));
                    spi_trigger_hit[i] = FALSE;
                } 
            } 
        } 
        
        if (PSOC_state == execution_state) {
            switch(RPi_Command) {      
                case read_gpio:
                    response_value = GPIO_Status_Reg_Read(); 
                    // SPIS_WriteTxDataZero(GPIO_Status_Reg_Read());
                    break;
                    
                case write_gpio:
                    GPIO_Control_Reg_Write(RPi_Data);
                    break;
                    
                case read_spi:
                    if ((RPi_Command_Data & PORT_MASK) == 0x0010) { 
                        response_value = ReadWriteSPIM1(RPi_Command_Data & DATA_MASK, 0x0000); 
                    } else if ((RPi_Command & PORT_MASK) == 0x0020) { 
                        response_value = ReadWriteSPIM2(RPi_Command_Data & DATA_MASK, 0x0000); 
                    }
                    break;
                
                case write_spi:
                    if ((RPi_Command_Data & PORT_MASK) == 0x0010) {
                        ReadWriteSPIM1(RPi_Command_Data & DATA_MASK, RPi_Data);
                    } else if ((RPi_Command_Data & PORT_MASK) == 0x0020) {
                        ReadWriteSPIM2(RPi_Command_Data & DATA_MASK, RPi_Data);
                    }
                    break;    
                
                case write_pwm: {
                    uint16 port = RPi_Command_Data & PORT_MASK;
                    uint16 parameter = RPi_Command_Data & 0x000F;
                    if (port == 0x0010) {
                        if (parameter == 0x0000) {
                            PWM_1_SetCompareMode(RPi_Data);
                        } else if (parameter == 0x0001) {
                            PWM_1_WritePeriod(RPi_Data);
                        } else if (parameter == 0x0002) {
                            PWM_1_WriteCompare(RPi_Data);
                        }
                    } else if (port == 0x0020) {
                        if (parameter == 0x0000) {
                            PWM_2_SetCompareMode(RPi_Data);
                        } else if (parameter == 0x0001) {
                            PWM_2_WritePeriod(RPi_Data);
                        } else if (parameter == 0x0002) {
                            PWM_2_WriteCompare(RPi_Data);
                        }
                    }
                }
                break;
                    
                case read_i2c: {
                        uint8 i2c_data_read;
                        if ((RPi_Command_Data & DATA_MASK) == 1) {
                            I2C_1_MasterReadBuf(RPi_Data >> 8, &i2c_data_read, 1, I2C_1_MODE_COMPLETE_XFER);
                            response_value = i2c_data_read; 
                        } else if ((RPi_Command_Data & DATA_MASK) == 2) {
                            I2C_2_MasterReadBuf(RPi_Data >> 8, &i2c_data_read, 1, I2C_2_MODE_COMPLETE_XFER);
                            response_value = i2c_data_read; 
                        }  
                    }
                    break;       
                
                case write_i2c:
                    if ((RPi_Command_Data & DATA_MASK) == 1) {
                        I2C_1_MasterWriteBuf(i2c_address, i2c_data_to_write, i2c_byte_count,  I2C_1_MODE_COMPLETE_XFER);
                    } else if ((RPi_Command_Data & DATA_MASK) == 2) {
                        I2C_2_MasterWriteBuf(i2c_address, i2c_data_to_write,  i2c_byte_count + 1,  I2C_2_MODE_COMPLETE_XFER);
                    }
                
                    i2c_byte_count = 0;
                    break;     
                
                case add_i2c_data:
                    if (i2c_byte_count < 8) {
                        i2c_data_to_write[i2c_byte_count] = (uint8)(0x00FF & RPi_Data);
                        i2c_byte_count++;
                    }
                    break; 
                
                case add_i2c_address:
                    i2c_address = RPi_Data;
                    break; 
                
                case set_spi_trigger:
                    spi_trigger_value[RPi_Command_Data & ORDINAL_MASK] = RPi_Data;
                    if ((RPi_Command_Data & TRIGGER_RESET_MASK) == 0x10) {
                        spi_trigger_reset[RPi_Command_Data & ORDINAL_MASK] = TRUE;
                    }
                    break;

                case set_trigger_radius:
                    spi_trigger_radius[RPi_Command_Data & ORDINAL_MASK] = RPi_Data;
                    break;
                    
                case read_encoder: {
                    uint8 port = (RPi_Command_Data & PORT_MASK) >> 0x4;
                    uint8 channel = RPi_Command_Data & CHANNEL_MASK;
                    response_value = ReadEncoder(port, channel);
                    break;
                }
                
                case set_pinmode: 
                    pinmode = RPi_Data; 
                    break; 
                 
                case read_firmware_date: {
                    response_value = firmwareVersionDate[RPi_Command_Data & ORDINAL_MASK]; 
                    break; 
                }
                
                case no_command:
                default:
                    break;
            }
        
            if (readiness == not_ready) { 
                readiness = ready;
                SPIS_WriteTxDataZero(READY); 
            } else if (readiness == NA) { 
                PSOC_state = idle_state; 
            } 
 
            SPIS_ClearRxBuffer();
        }
    }
}

uint16 ReadWriteSPIM1(uint8 ChannelNumber, uint8 data) {
    Control_Reg_SS_1_Write(ChannelNumber);
    SPIM_1_ClearFIFO();
    SPIM_1_WriteTxData(data);
    
    while(!(SPIM_1_ReadTxStatus() & SPIM_1_STS_SPI_DONE));
    uint16 result = SPIM_1_ReadRxData();
    return(result);
}

uint16 ReadWriteSPIM2(uint8 ChannelNumber, uint16 data) {
    Control_Reg_SS_2_Write(ChannelNumber);
    SPIM_2_ClearFIFO();
    SPIM_2_WriteTxData(data);
    
    while(!(SPIM_2_ReadTxStatus() & SPIM_2_STS_SPI_DONE));
    uint16 result = SPIM_2_ReadRxData();
    return(result);
}

uint16 ReadEncoder(uint8 port, uint8 ChannelNumber) {
    uint16 MSB = 0xff;
    uint16 LSB = 0xff;

    if (port == 0x01) {
        ReadWriteSPIM1(ChannelNumber, READ_ENCODER);
        while (ReadWriteSPIM1(ChannelNumber, 0x00) == ENCODER_IDLE) {}
        MSB = ReadWriteSPIM1(ChannelNumber, 0x00);
        LSB = ReadWriteSPIM1(ChannelNumber, 0x00);
   } else if (port == 0x02) {
        ReadWriteSPIM2(ChannelNumber, READ_ENCODER);
        while (ReadWriteSPIM2(ChannelNumber, 0x00) == ENCODER_IDLE) {}
        MSB = ReadWriteSPIM2(ChannelNumber, 0x00);
        LSB = ReadWriteSPIM2(ChannelNumber, 0x00);
   }

   return (uint16)(LSB + (MSB << 8));
}

/* QWJvbGlzaCB3YWdliGxhYm9yIG5vdyE= */
/* [] END OF FILE */
