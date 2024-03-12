from mojo import context
from ele_lib import muse_pulse

# MUSE-3300 ---------------------------------------------------------------------------------------
dvMUSE = context.devices.get("idevice")
dvREL = dvMUSE.relay
dvIR = dvMUSE.ir[0]
dvIO = dvMUSE.io

# VARIA-100 ---------------------------------------------------------------------------------------
dvVARIA = context.devices.get("AMX-10001")
dvTP = dvVARIA.port[1]

# PULSE用オブジェクト生成 ----------------------------------------------------------------------------------
pl = muse_pulse.Pulse()


# ボタン操作 -------------------------------------------------------------------------------------------
def ButtonEvent(e):
    ch = int(e.id)

    dvTP.channel[ch] = e.value

    if e.value: # PUSH
        if ch == 1:
            pl.pulse_muse_relay(dvREL,0,5)
        elif ch == 2:
            pl.pulse_muse_relay(dvREL,1,10)
        elif ch == 3:
            pl.pulse_muse_relay(dvREL,2,20)
        
        elif ch == 11:
            pl.pulse_muse_ir(dvIR,1,5)
        elif ch == 12:
            pl.pulse_muse_ir(dvIR,2,5)
        
        elif ch == 21:
            pl.pulse_muse_io(dvIO,0,5)
        elif ch == 22:
            pl.pulse_muse_io(dvIO,1,10)
        elif ch == 23:
            pl.pulse_muse_io(dvIO,2,20)
        
        elif ch == 31:
            pl.pulse_netlinx(dvTP,41,5)
        elif ch == 32:
            pl.pulse_netlinx(dvTP,42,10)
        elif ch == 33:
            pl.pulse_netlinx(dvTP,43,20)
        
        elif ch == 51:
            for i in range(8):
                pl.pulse_muse_relay(dvREL,i,10)
        elif ch == 52:
            for i in range(8):
                pl.pulse_muse_io(dvIO,i,10)


# リレーチャンネルイベント ------------------------------------------------------------------------------------
def RelayEvent(e):
    for ch in range(8):
        dvTP.channel[101 + ch] = dvREL[ch].state.value

# I/Oチャンネルイベント ------------------------------------------------------------------------------------
def IOEvent(e):
    for ch in range(8):
        dvTP.channel[111 + ch] = dvIO[ch].output.value


# イベント取得 ------------------------------------------------------------------------------------------
ev_ch = [1,2,3,11,12,21,22,23,31,32,33,51,52]
for ch in ev_ch:
    dvTP.button[ch].watch(ButtonEvent)

for ch in range(8):
    dvREL[ch].state.watch(RelayEvent)
    dvIO[ch].output.watch(IOEvent)

context.run(globals())