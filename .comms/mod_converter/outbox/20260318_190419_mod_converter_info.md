---
from: mod_converter
to: qa_lead
type: info
priority: low
---

FINISHED: Added @lint-ok MANUAL-AIM to 9 utility mods (Jackhammer, C4, Remote_Explosives, Vacuum_Cleaner, Welding_Tool, Winch, Magic_Bag, Swap_Button, Thruster_Tool). All use QueryRaycast for non-aim purposes (placement, pickup, surface detection, floor distance). Findings reduced 52→41, clean mods 69→78. Remaining 41 findings are gun mods (api_surgeon domain) or shared utils.