# -*- coding: utf-8 -*-
#%%
def resistance_query(address,channel):

    """
    ========== DESCRIPTION ==========

    This function can return the measured resistance of a channel

    ========== FROM ==========

    Manual of Lakeshore 370 on https://www.lakeshore.com/

    ========== INPUT ==========

    <address>
        -- string --
        The address of the instrument 

    <channel>
        -- int --
        The channel of the instrument from 1 to 16
        
    ========== OUTPUT ==========

    <resistance>
        -- float --
        The measured resistance of the channel
        [Ohm]
        
    ========== STATUS ==========

    Status : Checked

    ========= EXAMPLE ==========
    
    """

    ################## MODULES ################################################

    import pyvisa

    ################## INITIALISATION #########################################

    instru = pyvisa.ResourceManager().open_resource(address)

    channel = str(channel)
    answer = instru.query('RDGR? '+channel)
    resistance = float(answer)
    
    ################## FUNCTION ###############################################
    
    return resistance

#%%
def temperature_query(address,channel):

    """
    ========== DESCRIPTION ==========

    This function can return the measured temperature of a channel

    ========== FROM ==========

    Manual of Lakeshore 370 on https://www.lakeshore.com/

    ========== INPUT ==========

    <address>
        -- string --
        The address of the instrument 

    <channel>
        -- int --
        The channel of the instrument from 1 to 16
        
    ========== OUTPUT ==========

    <temperature>
        -- float --
        The measured temperature of the channel
        [K]
        
    ========== STATUS ==========

    Status : Checked

    ========= EXAMPLE ==========
    
    """

    ################## MODULES ################################################

    import pyvisa

    ################## INITIALISATION #########################################

    instru = pyvisa.ResourceManager().open_resource(address)

    channel = str(channel)
    answer = instru.query('RDGK? '+channel)
    temperature = float(answer)
    
    ################## FUNCTION ###############################################
    
    return temperature

#%%
def power_query(address,channel):

    """
    ========== DESCRIPTION ==========

    This function can return the injected power on a channel

    ========== FROM ==========

    Manual of Lakeshore 370 on https://www.lakeshore.com/

    ========== INPUT ==========

    <address>
        -- string --
        The address of the instrument 

    <channel>
        -- int --
        The channel of the instrument from 1 to 16
        
    ========== OUTPUT ==========

    <power>
        -- float --
        The injected power on the channel
        [W]
        
    ========== STATUS ==========

    Status : Checked

    ========= EXAMPLE ==========
    
    """

    ################## MODULES ################################################

    import pyvisa

    ################## INITIALISATION #########################################

    instru = pyvisa.ResourceManager().open_resource(address)

    channel = str(channel)
    answer = instru.query('RDGPWR? '+channel)
    power = float(answer)
    
    ################## FUNCTION ###############################################
    
    return power

#%%
def heater_range_command(address,value):

    """
    ========== DESCRIPTION ==========

    This function can setup the heater range of the heater output

    ========== FROM ==========

    Manual of Lakeshore 370 on https://www.lakeshore.com/

    ========== INPUT ==========

    <address>
        -- string --
        The address of the instrument 

    <value>
        -- int --
        The heater range (0 = Off
                          1 = 31.6 uA
                          2 = 100 uA
                          3 = 316 uA
                          4 = 1 mA
                          5 = 3.16 mA
                          6 = 10 mA
                          7 = 31.6 mA
                          8 = 100 mA)
        
    ========== STATUS ==========

    Status : Checked

    ========= EXAMPLE ==========
    
    """

    ################## MODULES ################################################

    import pyvisa

    ################## INITIALISATION #########################################

    instru = pyvisa.ResourceManager().open_resource(address)
    value = str(value)

    ################## FUNCTION ###############################################
    
    instru.write('HTRRNG '+value)
    
    return 

#%%
def heater_output_command(address,output):

    """
    ========== DESCRIPTION ==========

    This function can setup the heater output 

    ========== FROM ==========

    Manual of Lakeshore 370 on https://www.lakeshore.com/

    ========== INPUT ==========

    <address>
        -- string --
        The address of the instrument 

    <output>
        -- float --
        The heater output 
        [%]
        
    ========== STATUS ==========

    Status : Checked

    ========= EXAMPLE ==========
    
    """

    ################## MODULES ################################################

    import pyvisa

    ################## INITIALISATION #########################################

    instru = pyvisa.ResourceManager().open_resource(address)
    output = str(output)

    ################## FUNCTION ###############################################
    
    instru.write('MOUT ' + output)

    return 

#%%
def scan_query(address):

    """
    ========== DESCRIPTION ==========

    This function can return the scan mode of a channel

    ========== FROM ==========

    Manual of Lakeshore 370 on https://www.lakeshore.com/

    ========== INPUT ==========

    <address>
        -- string --
        The address of the instrument 
        
    ========== OUTPUT ==========

    <channel>
        -- int --
        The channel of the instrument from 1 to 16
        
    <scan_mode>
        -- int --
        The scan mode of a channel (0 = Autoscan off
                                    1 = Autoscan on)
    ========== STATUS ==========

    Status : Checked

    ========= EXAMPLE ==========
    
    """

    ################## MODULES ################################################

    import pyvisa

    ################## INITIALISATION #########################################

    instru = pyvisa.ResourceManager().open_resource(address)
    answer = instru.query('SCAN?')
    
    channel = int(answer[0:2])
    scan_mode = int(answer[3:4])
    
    ################## FUNCTION ###############################################
    
    return channel,scan_mode

#%%
def scan_command(address,channel,scan_mode):

    """
    ========== DESCRIPTION ==========

    This function can return the scan mode of the bridge

    ========== FROM ==========

    Manual of Lakeshore 370 on https://www.lakeshore.com/

    ========== INPUT ==========

    <address>
        -- string --
        The address of the instrument 

    <channel>
        -- int --
        The channel of the instrument from 1 to 16
        
    <scan_mode>
        -- int --
        The scan mode of the bridge (0 = Autoscan off
                                     1 = Autoscan on)
        
    ========== STATUS ==========

    Status : Checked

    ========= EXAMPLE ==========
    
    """

    ################## MODULES ################################################

    import pyvisa

    ################## INITIALISATION #########################################

    instru = pyvisa.ResourceManager().open_resource(address)
    channel = str(channel)
    scan_mode = str(scan_mode)

    ################## FUNCTION ###############################################
    
    instru.write('SCAN '+ channel + ',' + scan_mode) 
    
    return 

#%%
def resistance_range_command(address,channel,mode,excitation,range_value,autorange,autoexcitation):

    """
    ========== DESCRIPTION ==========

    This function can setup the resistance reading of a channel

    ========== FROM ==========

    Manual of Lakeshore 370 on https://www.lakeshore.com/

    ========== INPUT ==========

    <address>
        -- string --
        The address of the instrument 

    <channel>
        -- int --
        The channel of the instrument from 1 to 16 (0 = All channels)

    <mode>
        -- int --
        The excitation mode (0 = voltage
                             1 = current)

    <excitation>
        -- int --
        The excitation range (1 = 2 uV      /   1 pA 
                              2 = 6.32 uV   /   3.16 pA
                              3 = 20 uV     /   10 pA
                              4 = 63.2 uV   /   31.6 pA
                              5 = 200 uV    /   100 pA
                              6 = 632 uV    /   316 pA
                              7 = 2 mV      /   1 nA
                              8 = 6.32 mV   /   3.16 nA
                              9 = 20 mV     /   10 nA
                              10 = 63.2 mV  /   31.6 nA
                              11 = 200 mV   /   100 nA
                              12 = 632 mV   /   316 nA
                              13 =          /   1 uA
                              14 =          /   3.16 uA
                              15 =          /   10 uA
                              16 =          /   31.6 uA
                              17 =          /   100 uA
                              18 =          /   316 uA
                              19 =          /   1 mA
                              20 =          /   3.16 mA
                              21 =          /   10 muA
                              22 =          /   31.6 mA)

    <range_value>
        -- int --
        The resistance range (1 = 2 mOhm
                              2 = 6.32 mOhm
                              3 = 20 mOhm
                              4 = 63.2 mOhm
                              5 = 200 mOhm
                              6 = 632 mOhm
                              7 = 2 Ohm
                              8 = 6.32 Ohm
                              9 = 20 Ohm
                              10 = 63.2 Ohm
                              11 = 200 Ohm
                              12 = 632 Ohm
                              13 = 2 kOhm
                              14 = 6.32 kOhm
                              15 = 20 kOhm
                              16 = 63.2 kOhm
                              17 = 200 kOhm
                              18 = 632 kOhm
                              19 = 2 MOhm
                              20 = 6.32 MOhm
                              21 = 20 MOhm
                              22 = 63.2 MOhm)
        
    <autorange>
        -- int --
        The autorange mode (0 = autorange off
                            1 = autorange on)

    <autoexcitation>
        -- int --
        The autoexcitation mode (0 = autoexcitation on
                                 1 = autoexcitation off)

    ========== STATUS ==========

    Status : Checked

    ========= EXAMPLE ==========
    
    """

    ################## MODULES ################################################

    import pyvisa

    ################## INITIALISATION #########################################

    instru = pyvisa.ResourceManager().open_resource(address)
    channel = str(channel)
    mode = str(mode)
    excitation = str(excitation)
    range_value = str(range_value)
    autorange = str(autorange)
    autoexcitation = str(autoexcitation)

    ################## FUNCTION ###############################################
    
    instru.write('RDGRNG '+ channel + ',' + mode + ',' + excitation + ',' + range_value + ',' + autorange + ',' + autoexcitation)
    
    return 

#%%
def resistance_range_query(address,channel,mode,excitation,range_value,autorange,autoexcitation):

    """
    ========== DESCRIPTION ==========

    This function can return the resistance reading of a channel

    ========== FROM ==========

    Manual of Lakeshore 370 on https://www.lakeshore.com/

    ========== INPUT ==========

    <address>
        -- string --
        The address of the instrument 

    <channel>
        -- int --
        The channel of the instrument from 1 to 16 (0 = All channels)

    ========== OUTPUT ==========
    
    <mode>
        -- int --
        The excitation mode (0 = voltage
                             1 = current)
     
    <excitation>
        -- int --
        The excitation range (1 = 2 uV      /   1 pA 
                              2 = 6.32 uV   /   3.16 pA
                              3 = 20 uV     /   10 pA
                              4 = 63.2 uV   /   31.6 pA
                              5 = 200 uV    /   100 pA
                              6 = 632 uV    /   316 pA
                              7 = 2 mV      /   1 nA
                              8 = 6.32 mV   /   3.16 nA
                              9 = 20 mV     /   10 nA
                              10 = 63.2 mV  /   31.6 nA
                              11 = 200 mV   /   100 nA
                              12 = 632 mV   /   316 nA
                              13 =          /   1 uA
                              14 =          /   3.16 uA
                              15 =          /   10 uA
                              16 =          /   31.6 uA
                              17 =          /   100 uA
                              18 =          /   316 uA
                              19 =          /   1 mA
                              20 =          /   3.16 mA
                              21 =          /   10 muA
                              22 =          /   31.6 mA)
     
    <range_value>
        -- int --
        The resistance range (1 = 2 mOhm
                              2 = 6.32 mOhm
                              3 = 20 mOhm
                              4 = 63.2 mOhm
                              5 = 200 mOhm
                              6 = 632 mOhm
                              7 = 2 Ohm
                              8 = 6.32 Ohm
                              9 = 20 Ohm
                              10 = 63.2 Ohm
                              11 = 200 Ohm
                              12 = 632 Ohm
                              13 = 2 kOhm
                              14 = 6.32 kOhm
                              15 = 20 kOhm
                              16 = 63.2 kOhm
                              17 = 200 kOhm
                              18 = 632 kOhm
                              19 = 2 MOhm
                              20 = 6.32 MOhm
                              21 = 20 MOhm
                              22 = 63.2 MOhm)
        
    <autorange>
        -- int --
        The autorange mode (0 = autorange off
                            1 = autorange on)
     
    <autoexcitation>
        -- int --
        The autoexcitation mode (0 = autoexcitation on
                                 1 = autoexcitation off)

    ========== STATUS ==========

    Status : Checked

    ========= EXAMPLE ==========
    
    """

    ################## MODULES ################################################

    import pyvisa

    ################## INITIALISATION #########################################

    instru = pyvisa.ResourceManager().open_resource(address)
    channel = str(channel)

    answer = instru.query('RDGRNG? ' + channel)
    
    mode = answer[0:1]
    excitation = answer[2:4]
    range_value = answer[5:7]
    autorange = answer[8:9]
    autoexcitation = answer[10:11]
    
    ################## FUNCTION ###############################################
    
    return mode,excitation,range_value,autorange,autoexcitation


#%%
def heater_range_query(address):

    """
    ========== DESCRIPTION ==========

    This function can return the heater range of the heater output

    ========== FROM ==========

    Manual of Lakeshore 370 on https://www.lakeshore.com/

    ========== INPUT ==========

    <address>
        -- string --
        The address of the instrument 
        
    ========== OUTPUT ==========
       
    <value>
        -- int --
        The heater range (0 = Off
                          1 = 31.6 uA
                          2 = 100 uA
                          3 = 316 uA
                          4 = 1 mA
                          5 = 3.16 mA
                          6 = 10 mA
                          7 = 31.6 mA
                          8 = 100 mA)
        
    ========== STATUS ==========

    Status : Checked

    ========= EXAMPLE ==========
    
    """

    ################## MODULES ################################################

    import pyvisa

    ################## INITIALISATION #########################################

    instru = pyvisa.ResourceManager().open_resource(address)
    answer = instru.query('HTRRNG?')
    value = float(answer)
    
    ################## FUNCTION ###############################################

    return value

#%%
def heater_output_query(address):

    """
    ========== DESCRIPTION ==========

    This function can setup the heater output 

    ========== FROM ==========

    Manual of Lakeshore 370 on https://www.lakeshore.com/

    ========== INPUT ==========

    <address>
        -- string --
        The address of the instrument 
        
    ========== OUTPUT ==========

    <output>
        -- float --
        The heater output 
        [%]
        
    ========== STATUS ==========

    Status : Checked

    ========= EXAMPLE ==========
    
    """

    ################## MODULES ################################################

    import pyvisa

    ################## INITIALISATION #########################################

    instru = pyvisa.ResourceManager().open_resource(address)
    answer = instru.query('HTR?')
    output = float(answer)
    
    ################## FUNCTION ###############################################

    return output

#%%
def temperature_control_mode_command(address,mode):

    """
    ========== DESCRIPTION ==========

    This function can setup the temperature control mode 

    ========== FROM ==========

    Manual of Lakeshore 370 on https://www.lakeshore.com/

    ========== INPUT ==========

    <address>
        -- string --
        The address of the instrument 
        
    <mode>
        -- int --
        The temperature control mode (1 = Closed-loop PID
                                      2 = Zone tuning
                                      3 = Open loop
                                      4 = Off)
        
    ========== STATUS ==========

    Status : Checked

    ========= EXAMPLE ==========
    
    """

    ################## MODULES ################################################

    import pyvisa

    ################## INITIALISATION #########################################

    instru = pyvisa.ResourceManager().open_resource(address)
    mode = str(mode)

    ################## FUNCTION ###############################################
    
    instru.write('CMODE '+ mode) 
    
    return 

#%%
def temperature_control_mode_query(address):

    """
    ========== DESCRIPTION ==========

    This function can return the temperature control mode 

    ========== FROM ==========

    Manual of Lakeshore 370 on https://www.lakeshore.com/

    ========== INPUT ==========

    <address>
        -- string --
        The address of the instrument 
    
    ========== OUTPUT ==========   
    
    <mode>
        -- int --
        The temperature control mode (1 = Closed-loop PID
                                      2 = Zone tuning
                                      3 = Open loop
                                      4 = Off)
        
    ========== STATUS ==========

    Status : Checked

    ========= EXAMPLE ==========
    
    """

    ################## MODULES ################################################

    import pyvisa

    ################## INITIALISATION #########################################

    instru = pyvisa.ResourceManager().open_resource(address)
    answer = instru.query('CMODE?')
    mode = int(answer)

    ################## FUNCTION ###############################################
    
    return mode

#%%
def channel_parameter_query(address,channel):

    """
    ========== DESCRIPTION ==========

    This function can return the channel parameters

    ========== FROM ==========

    Manual of Lakeshore 370 on https://www.lakeshore.com/

    ========== INPUT ==========

    <address>
        -- string --
        The address of the instrument 

    <channel>
        -- int --
        The channel of the instrument from 1 to 16
    
    ========== OUTPUT ==========   
    
    <channel_status>
        -- int --
        The status of the channel (0 = Off
                                   1 = On)
        
    <dwell>
        -- int --
        The dwell time of the channel   
        [s]
        
    <pause>
        -- int --
        The pause time of the channel   
        [s]

    <curve_number>
        -- int --
        The curve number of the channel

    <coefficient>
        -- int --
        The temperature coefficient (1 = negative
                                     2 = positive)             
        
    ========== STATUS ==========

    Status : Checked

    ========= EXAMPLE ==========
    
    """

    ################## MODULES ################################################

    import pyvisa

    ################## INITIALISATION #########################################

    instru = pyvisa.ResourceManager().open_resource(address)
    channel = str(channel)
    answer = instru.query('INSET? ' + channel)
    channel_status = int(answer[0:1])
    dwell = int(answer[2:5])
    pause = int(answer[6:9])
    curve_number = int(answer[10:12])
    coefficient = int(answer[13:14])
    
    ################## FUNCTION ###############################################
    
    return channel_status,dwell,pause,curve_number,coefficient

#%%
def channel_parameter_command(address,channel,channel_status,dwell,pause,curve_number,coefficient):

    """
    ========== DESCRIPTION ==========

    This function can setup the channel parameters

    ========== FROM ==========

    Manual of Lakeshore 370 on https://www.lakeshore.com/

    ========== INPUT ==========

    <address>
        -- string --
        The address of the instrument 

    <channel>
        -- int --
        The channel of the instrument from 1 to 16 
    
    <channel_status>
        -- int --
        The status of the channel (0 = Off
                                   1 = On)
        
    <dwell>
        -- int --
        The dwell time of the channel   
        [s]
        
    <pause>
        -- int --
        The pause time of the channel   
        [s]

    <curve_number>
        -- int --
        The curve number of the channel

    <coefficient>
        -- int --
        The temperature coefficient (1 = negative
                                     2 = positive)             
        
    ========== STATUS ==========

    Status : Checked

    ========= EXAMPLE ==========
    
    """
    ################## MODULES ################################################

    import pyvisa

    ################## INITIALISATION #########################################

    instru = pyvisa.ResourceManager().open_resource(address)
    channel = str(channel)
    channel_status = str(channel_status)
    dwell = str(dwell)
    pause = str(pause)
    curve_number = str(curve_number)
    coefficient = str(coefficient)
    
    ################## FUNCTION ###############################################
    
    instru.write('INSET ' + channel + ',' + channel_status + ',' + dwell + ',' + pause + ',' + curve_number + ',' + coefficient)
    return 

#%%
def interface_mode_command(address,interface_mode):

    """
    ========== DESCRIPTION ==========

    This function can setup the interface mode

    ========== FROM ==========

    Manual of Lakeshore 370 on https://www.lakeshore.com/

    ========== INPUT ==========

    <address>
        -- string --
        The address of the instrument 

    <interface_mode>
        -- int --
        The interface mode (0 = local
                            1 = remote
                            2 = remote with local lockout)             
        
    ========== STATUS ==========

    Status : Checked

    ========= EXAMPLE ==========
    
    """
    ################## MODULES ################################################

    import pyvisa

    ################## INITIALISATION #########################################

    instru = pyvisa.ResourceManager().open_resource(address)
    interface_mode = str(interface_mode)
    
    ################## FUNCTION ###############################################
    
    instru.write('MODE ' + interface_mode)
    return 

#%%
def interface_mode_query(address):

    """
    ========== DESCRIPTION ==========

    This function can setup the interface mode

    ========== FROM ==========

    Manual of Lakeshore 370 on https://www.lakeshore.com/

    ========== INPUT ==========

    <address>
        -- string --
        The address of the instrument 

    ========== OUTPUT ==========
    
    <interface_mode>
        -- int --
        The interface mode (0 = local
                            1 = remote
                            2 = remote with local lockout)             
        
    ========== STATUS ==========

    Status : Checked

    ========= EXAMPLE ==========
    
    """
    ################## MODULES ################################################

    import pyvisa

    ################## INITIALISATION #########################################

    instru = pyvisa.ResourceManager().open_resource(address)
    answer = instru.query('MODE?')
    interface_mode = int(answer)
    
    ################## FUNCTION ###############################################
    
    return interface_mode

#%%
def pid_parameters_query(address):

    """
    ========== DESCRIPTION ==========

    This function can return the pid parameters

    ========== FROM ==========

    Manual of Lakeshore 370 on https://www.lakeshore.com/

    ========== INPUT ==========

    <address>
        -- string --
        The address of the instrument 

    ========== OUTPUT ==========
    
    <p>
        -- float --
        The "p" parameter
    []

    <i>
        -- int --
        The "i" parameter
    [s]

    <d>
        -- int --
        The "d" parameter
    [s]
         
    ========== STATUS ==========

    Status : Checked

    ========= EXAMPLE ==========
    
    """
    ################## MODULES ################################################

    import pyvisa

    ################## INITIALISATION #########################################

    instru = pyvisa.ResourceManager().open_resource(address)
    answer = instru.query('MODE?')
    p = float(answer[0:7])
    i = int(answer[9:15])
    d = int(answer[17:23])
    
    ################## FUNCTION ###############################################
    
    return p,i,d

#%%
def pid_parameters_command(address,p,i,d):

    """
    ========== DESCRIPTION ==========

    This function can setup the pid parameters

    ========== FROM ==========

    Manual of Lakeshore 370 on https://www.lakeshore.com/

    ========== INPUT ==========

    <address>
        -- string --
        The address of the instrument 
    
    <p>
        -- float --
        The "p" parameter
    []

    <i>
        -- int --
        The "i" parameter
    [s]

    <d>
        -- int --
        The "d" parameter
    [s]
         
    ========== STATUS ==========

    Status : Checked

    ========= EXAMPLE ==========
    
    """
    ################## MODULES ################################################

    import pyvisa

    ################## INITIALISATION #########################################

    instru = pyvisa.ResourceManager().open_resource(address)
    p = str(p)
    i = str(i)
    d = str(d)
    
    ################## FUNCTION ###############################################
    
    instru.write('PID ' + p + ',' + i + ',' + d)
    
    return 