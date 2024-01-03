import pymem.process
import keyboard
import pymem
import time
from pynput.mouse import Controller, Button
from random import uniform

from offsets import OffsetManager

mouse = Controller()
offsetManager = OffsetManager()

dwEntityList = offsetManager.offset('dwEntityList')
dwLocalPlayerPawn = offsetManager.offset('dwLocalPlayerPawn')
m_hPlayerPawn = offsetManager.get('CCSPlayerController', 'm_hPlayerPawn')
m_iIDEntIndex = offsetManager.get('C_CSPlayerPawnBase', 'm_iIDEntIndex')
m_iTeamNum = offsetManager.get('C_BaseEntity', 'm_iTeamNum')
m_iHealth = offsetManager.get('C_BaseEntity', 'm_iHealth')
m_flDetectedByEnemySensorTime = offsetManager.get('C_CSPlayerPawnBase', 'm_flDetectedByEnemySensorTime')

triggerKey = "shift"


def glow(client, pm):
    try:
        for i in range(1, 64):
            entity_list = pm.read_longlong(client + dwEntityList)
            if entity_list == 0:
                continue
            list_entry = pm.read_longlong(entity_list + (8 * (i & 0x7FFF) >> 9) + 16)
            if list_entry == 0:
                continue
            player = pm.read_longlong(list_entry + 120 * (i & 0x1FF))
            if player == 0:
                continue
            player_pawn = pm.read_longlong(player + m_hPlayerPawn)
            list_entry2 = pm.read_longlong(entity_list + 0x8 * ((player_pawn & 0x7FFF) >> 9) + 16)
            if list_entry2 == 0:
                continue
            p_cs_player_pawn = pm.read_longlong(list_entry2 + 120 * (player_pawn & 0x1FF))
            if p_cs_player_pawn == 0:
                continue
            pm.write_float(p_cs_player_pawn + m_flDetectedByEnemySensorTime, float(100000))
    except:
        pass


def trigger(client, pm):
    try:
        if keyboard.is_pressed(triggerKey):
            player = pm.read_longlong(client + dwLocalPlayerPawn)
            entity_id = pm.read_int(player + m_iIDEntIndex)

            if entity_id > 0:
                ent_list = pm.read_longlong(client + dwEntityList)

                ent_entry = pm.read_longlong(ent_list + 0x8 * (entity_id >> 9) + 0x10)
                entity = pm.read_longlong(ent_entry + 120 * (entity_id & 0x1FF))

                entity_team = pm.read_int(entity + m_iTeamNum)
                player_team = pm.read_int(player + m_iTeamNum)

                if entity_team != player_team:
                    entity_hp = pm.read_int(entity + m_iHealth)
                    if entity_hp > 0:
                        time.sleep(uniform(0.01, 0.03))
                        mouse.press(Button.left)
                        time.sleep(uniform(0.01, 0.05))
                        mouse.release(Button.left)
    except:
        pass


def main():
    pm = pymem.Pymem("cs2.exe")
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
    print("Cheat made by ximik753 (https://github.com/ximik753/cs2-cheat)")
    print(f'[-] Cheat started\n. [-]Trigger bot key: {triggerKey.upper()}')

    while True:
        try:
            trigger(client, pm)
            glow(client, pm)
        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    main()
