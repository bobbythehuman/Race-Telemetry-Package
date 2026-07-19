import ctypes
from enum import Enum, IntEnum

# source
# https://www.assettocorsa.net/forum/index.php?threads/shared-memory-api-documentation.83659/
# https://docs.google.com/document/d/1WzqMLkW2o_C0LGcvdMRelAV31ZIifux0CSHD9k6ddz0/edit?tab=t.0

class DataTypes:
    STRUCTURE = ctypes.LittleEndianStructure
    
    SIGNED_INT = ctypes.c_int
    SIGNED_INT8 = ctypes.c_int8
    SIGNED_INT32 = ctypes.c_int32
    
    UNSIGNED_INT8 = ctypes.c_uint8
    UNSIGNED_INT32 = ctypes.c_uint32
    UNSIGNED_INT64 = ctypes.c_uint64
    FLOAT = ctypes.c_float
    
    SIGNED_SHORT = ctypes.c_short
    UNSIGNED_SHORT = ctypes.c_ushort
    
    BOOL = ctypes.c_bool
    CHAR = ctypes.c_wchar


### * Enums

class ACEVO_STATUS(IntEnum):
    AC_OFF = 0      # Simulator is not running / no session active
    AC_REPLAY = 1   # A replay is currently being played back
    AC_LIVE = 2     # Live driving session is active
    AC_PAUSE = 3    # Session is paused

class ACEVO_SESSION_TYPE(IntEnum):
    AC_UNKNOWN = -1     # Session type not yet determined
    AC_TIME_ATTACK = 0  # Time attack / qualifying session
    AC_RACE = 1         # Race session
    AC_HOT_STINT = 2    # Hot-stint practice
    AC_CRUISE = 3       # Untimed cruise

class ACEVO_FLAG_TYPE(IntEnum):
    AC_NO_FLAG = 0                      # No flag displayed
    AC_WHITE_FLAG = 1                   # Slow vehicle ahead on track
    AC_GREEN_FLAG = 2                   # Track clear — racing resumed
    AC_RED_FLAG = 3                     # Session stopped due to incident or hazard
    AC_BLUE_FLAG = 4                    # Lapped car must yield to the race leader
    AC_YELLOW_FLAG = 5                  # Hazard present — no overtaking
    AC_BLACK_FLAG = 6                   # Driver disqualified / must pit immediately
    AC_BLACK_WHITE_FLAG = 7             # Warning for unsportsmanlike behaviour
    AC_CHECKERED_FLAG = 8               # Session or race has ended
    AC_ORANGE_CIRCLE_FLAG = 9           # Mechanical problem — car must pit
    AC_RED_YELLOW_STRIPES_FLAG = 10     # Slippery surface ahead on track

class ACEVO_CAR_LOCATION(IntEnum):
    ACEVO_UNASSIGNED = 0    # Position not yet determined
    ACEVO_PITLANE = 1       # Car is inside the pit lane
    ACEVO_PITENTRY = 2      # Car is at the pit-lane entry
    ACEVO_PITEXIT = 3       # Car is at the pit-lane exit
    ACEVO_TRACK = 4         # Car is on the racing circuit

class ACEVO_ENGINE_TYPE(IntEnum):
    ACEVO_INTERNAL_COMBUSTION = 0   # Traditional petrol/diesel internal combustion engine
    ACEVO_ELECTRIC_MOTOR = 1        # Fully electric powertrain

class ACEVO_STARTING_GRIP(IntEnum):
    ACEVO_GREEN = 0     # Track grip at minimum
    ACEVO_FAST = 1      # Track grip in advanced (fast) stage
    ACEVO_OPTIMUM = 2   # Track conditions starting at optimum grip


### * Data Structure

# Complete state of a single tyre corner. Embedded four times in SPageFileGraphicEvo (lf, rf, lr, rr). [256 bytes]
class SMEvoTyreState(DataTypes.STRUCTURE):
    # _pack_ = 1
    _fields_ = [
        ("slip",                                DataTypes.FLOAT),     # Combined tyre slip magnitude
        ("lock",                                DataTypes.BOOL),      # Tyre is locked under braking (true = locking)
        ("tyre_pressure",                       DataTypes.FLOAT),     # Tyre inflation pressure (PSI)
        ("tyre_temperature_c",                  DataTypes.FLOAT),     # Average tyre carcass temperature in °C
        ("brake_temperature_c",                 DataTypes.FLOAT),     # Brake disc temperature in °C
        ("brake_pressure",                      DataTypes.FLOAT),     # Hydraulic brake pressure applied at this corner
        ("tyre_temperature_left",               DataTypes.FLOAT),     # Inner-edge tyre temperature in °C
        ("tyre_temperature_center",             DataTypes.FLOAT),     # Centre-tread tyre temperature in °C
        ("tyre_temperature_right",              DataTypes.FLOAT),     # Outer-edge tyre temperature in °C
        ("tyre_compound_front",                 DataTypes.CHAR * 33), # Name of the compound fitted on the front axle
        ("tyre_compound_rear",                  DataTypes.CHAR * 33), # Name of the compound fitted on the rear axle
        ("tyre_normalized_pressure",            DataTypes.FLOAT),     # Pressure as a 0–1 fraction of the target range
        ("tyre_normalized_temperature_left",    DataTypes.FLOAT),     # Inner-edge temperature as a 0–1 fraction of optimal range
        ("tyre_normalized_temperature_center",  DataTypes.FLOAT),     # Centre temperature as a 0–1 fraction of optimal range
        ("tyre_normalized_temperature_right",   DataTypes.FLOAT),     # Outer-edge temperature as a 0–1 fraction of optimal range
        ("brake_normalized_temperature",        DataTypes.FLOAT),     # Brake temperature as a 0–1 fraction of optimal operating range
        ("tyre_normalized_temperature_core",    DataTypes.FLOAT),     # Core tyre temperature as a 0–1 fraction of optimal range
    ]


# Structural damage level for each body zone of the car (0.0 = undamaged, 1.0 = destroyed). [128 bytes]
class SMEvoDamageState(DataTypes.STRUCTURE):
    # _pack_ = 1
    _fields_ = [
        ("damage_front",            DataTypes.FLOAT), # Damage on the front body / nose
        ("damage_rear",             DataTypes.FLOAT), # Damage on the rear body / diffuser
        ("damage_left",             DataTypes.FLOAT), # Damage on the left side of the body
        ("damage_right",            DataTypes.FLOAT), # Damage on the right side of the body
        ("damage_center",           DataTypes.FLOAT), # Damage on the central / underfloor area
        ("damage_suspension_lf",    DataTypes.FLOAT), # Damage on the front-left suspension
        ("damage_suspension_rf",    DataTypes.FLOAT), # Damage on the front-right suspension
        ("damage_suspension_lr",    DataTypes.FLOAT), # Damage on the rear-left suspension
        ("damage_suspension_rr",    DataTypes.FLOAT), # Damage on the rear-right suspension
    ]


# Status of each pit-stop service action. −1 = will not perform, 0 = completed, 1 = in progress. [64 bytes]
class SMEvoPitInfo(DataTypes.STRUCTURE):
    # _pack_ = 1
    _fields_ = [
        ("damage",      DataTypes.UNSIGNED_INT8), # Body-repair action state
        ("fuel",        DataTypes.UNSIGNED_INT8), # Refuelling action state
        ("tyres_lf",    DataTypes.UNSIGNED_INT8), # Front-left tyre change state
        ("tyres_rf",    DataTypes.UNSIGNED_INT8), # Front-right tyre change state
        ("tyres_lr",    DataTypes.UNSIGNED_INT8), # Rear-left tyre change state
        ("tyres_rr",    DataTypes.UNSIGNED_INT8), # Rear-right tyre change state
    ]


# All driver-adjustable electronic aid and setup settings. [128 bytes]
class SMEvoElectronics(DataTypes.STRUCTURE):
    # _pack_ = 1
    _fields_ = [
        ("tc_level",                    DataTypes.UNSIGNED_INT8),   # Traction-control level (0 = off, higher = more aggressive)
        ("tc_cut_level",                DataTypes.UNSIGNED_INT8),   # TC throttle-cut aggressiveness level
        ("abs_level",                   DataTypes.UNSIGNED_INT8),   # ABS intervention level (0 = off)
        ("esc_level",                   DataTypes.UNSIGNED_INT8),   # Electronic stability-control level (0 = off)
        ("ebb_level",                   DataTypes.UNSIGNED_INT8),   # Electronic brake-balance adjustment level
        ("brake_bias",                  DataTypes.FLOAT),           # Front brake-bias ratio (e.g. 0.56 = 56 % front)
        ("engine_map_level",            DataTypes.UNSIGNED_INT8),   # Engine map / power mode selection
        ("turbo_level",                 DataTypes.FLOAT),           # Turbo wastegate or boost target setting
        ("ers_deployment_map",          DataTypes.UNSIGNED_INT8),   # ERS power-deployment strategy map
        ("ers_recharge_map",            DataTypes.FLOAT),           # ERS recharge aggressiveness setting
        ("is_ers_heat_charging_on",     DataTypes.BOOL),            # ERS heat-based charging is enabled
        ("is_ers_overtake_mode_on",     DataTypes.BOOL),            # ERS overtake (maximum-deploy) mode is active
        ("is_drs_open",                 DataTypes.BOOL),            # DRS flap is currently open
        ("diff_power_level",            DataTypes.UNSIGNED_INT8),   # Differential lock level under power
        ("diff_coast_level",            DataTypes.UNSIGNED_INT8),   # Differential lock level on lift / coast
        ("front_bump_damper_level",     DataTypes.UNSIGNED_INT8),   # Front bump (compression) damper stiffness level
        ("front_rebound_damper_level",  DataTypes.UNSIGNED_INT8),   # Front rebound damper stiffness level
        ("rear_bump_damper_level",      DataTypes.UNSIGNED_INT8),   # Rear bump (compression) damper stiffness level
        ("rear_rebound_damper_level",   DataTypes.UNSIGNED_INT8),   # Rear rebound damper stiffness level
        ("is_ignition_on",              DataTypes.BOOL),            # Ignition switch is on
        ("is_pitlimiter_on",            DataTypes.BOOL),            # Pit-speed limiter is active
        ("active_performance_mode",     DataTypes.UNSIGNED_INT8),   # Selected vehicle performance / power mode index
    ]


# Cockpit light, display, and instrumentation panel states. [128 bytes]
class SMEvoInstrumentation(DataTypes.STRUCTURE):
    # _pack_ = 1
    _fields_ = [
        ("main_light_stage",            DataTypes.SIGNED_INT8),   # Main exterior light stage (0 = off)
        ("special_light_stage",         DataTypes.SIGNED_INT8),   # Auxiliary / special lights level
        ("cockpit_light_stage",         DataTypes.SIGNED_INT8),   # Interior cockpit illumination level
        ("wiper_level",                 DataTypes.SIGNED_INT8),   # Windscreen wiper speed (0 = off)
        ("rain_lights",                 DataTypes.BOOL),          # Rear rain light is on
        ("direction_light_left",        DataTypes.BOOL),          # Left turn indicator is active
        ("direction_light_right",       DataTypes.BOOL),          # Right turn indicator is active
        ("flashing_lights",             DataTypes.BOOL),          # Flashing lights are active
        ("warning_lights",              DataTypes.BOOL),          # Hazard lights are illuminated
        ("selected_display_index",      DataTypes.SIGNED_INT8),   # Index of the currently focused display device
        ("display_current_page_index",  DataTypes.SIGNED_INT8),   # Active page index on displays
        ("are_headlights_visible",      DataTypes.BOOL),          # Headlights are on and visible to other drivers
    ]


# Server-side session lifecycle information. [256 bytes]
class SMEvoSessionState(DataTypes.STRUCTURE):
    # _pack_ = 1
    _fields_ = [
        ("phase_name",                  DataTypes.CHAR * 15),       # Name of the current session phase (e.g. 'Race', 'Qualify')
        ("time_left",                   DataTypes.CHAR * 15),       # Formatted remaining session time (HH:MM:SS)
        ("time_left_ms",                DataTypes.SIGNED_INT32),    # Remaining session time in milliseconds
        ("wait_time",                   DataTypes.CHAR * 15),       # Formatted wait time before session start
        ("total_lap",                   DataTypes.SIGNED_INT32),    # Total laps scheduled for this session
        ("current_lap",                 DataTypes.SIGNED_INT32),    # Current lap number being driven
        ("lights_on",                   DataTypes.SIGNED_INT32),    # Number of starting lights currently illuminated
        ("lights_mode",                 DataTypes.SIGNED_INT32),    # Starting-light sequence mode identifier
        ("lap_length_km",               DataTypes.FLOAT),           # Track lap length in kilometres
        ("end_session_flag",            DataTypes.SIGNED_INT32),    # Non-zero when the session is ending
        ("time_to_next_session",        DataTypes.CHAR * 15),       # Formatted countdown to the next session
        ("disconnected_from_server",    DataTypes.BOOL),            # Player has lost connection to the game server
        ("restart_season_enabled",      DataTypes.BOOL),            # Season restart option is available to the player
        ("ui_enable_drive",             DataTypes.BOOL),            # Drive button is enabled in the UI
        ("ui_enable_setup",             DataTypes.BOOL),            # Setup screen is accessible from the UI
        ("is_ready_to_next_blinking",   DataTypes.BOOL),            # Ready-to-proceed indicator is blinking
        ("show_waiting_for_players",    DataTypes.BOOL),            # Waiting-for-players lobby screen is shown
    ]


# Lap timing and delta values displayed on the HUD. [256 bytes]
class SMEvoTimingState(DataTypes.STRUCTURE):
    # _pack_ = 1
    _fields_ = [
        ("current_laptime", DataTypes.CHAR * 15),     # Current lap time as a formatted string
        ("delta_current",   DataTypes.CHAR * 15),     # Delta vs. current reference lap (formatted)
        ("delta_current_p", DataTypes.SIGNED_INT32),  # Sign of delta_current: +1 slower, −1 faster, 0 = hidden
        ("last_laptime",    DataTypes.CHAR * 15),     # Last completed lap time as a formatted string
        ("delta_last",      DataTypes.CHAR * 15),     # Delta vs. last lap (formatted)
        ("delta_last_p",    DataTypes.SIGNED_INT32),  # Sign of delta_last: +1 slower, −1 faster, 0 = hidden
        ("best_laptime",    DataTypes.CHAR * 15),     # Personal best lap time as a formatted string
        ("ideal_laptime",   DataTypes.CHAR * 15),     # Theoretical best lap (sum of best sectors) as a formatted string
        ("total_time",      DataTypes.CHAR * 15),     # Total elapsed session time as a formatted string
        ("is_invalid",      DataTypes.BOOL),          # Current lap has been invalidated (track-limits violation, etc.)
    ]


# Driver-assist settings currently active for the player car. [64 bytes]
class SMEvoAssistsState(DataTypes.STRUCTURE):
    # _pack_ = 1
    _fields_ = [
        ("auto_gear",                   DataTypes.UNSIGNED_INT8), # Automatic gearshift aid level (0 = off)
        ("auto_blip",                   DataTypes.UNSIGNED_INT8), # Automatic throttle blip on downshift (0 = off)
        ("auto_clutch",                 DataTypes.UNSIGNED_INT8), # Automatic clutch management (0 = off)
        ("auto_clutch_on_start",        DataTypes.UNSIGNED_INT8), # Automatic clutch during the rolling start (0 = off)
        ("manual_ignition_e_start",     DataTypes.UNSIGNED_INT8), # Manual ignition and electric start required (0 = automatic)
        ("auto_pit_limiter",            DataTypes.UNSIGNED_INT8), # Pit-speed limiter activates automatically (0 = manual)
        ("standing_start_assist",       DataTypes.UNSIGNED_INT8), # Standing-start launch assistance active (0 = off)
        ("auto_steer",                  DataTypes.FLOAT),         # Auto-steer correction strength (0.0 = off, 1.0 = maximum)
        ("arcade_stability_control",    DataTypes.FLOAT),         # Arcade-style stability aid level (0.0 = off, 1.0 = maximum)
    ]


# Raw physics telemetry updated every simulation step. Contains all low-level vehicle dynamics data.
class SPageFilePhysicsData(DataTypes.STRUCTURE):
    # _pack_ = 1
    _fields_ = [
        ("packetId",            DataTypes.SIGNED_INT),    # Incrementing counter — detect new data packets by comparing to previous value
        ("gas",                 DataTypes.FLOAT),         # Throttle pedal position (0.0 = released, 1.0 = full throttle)
        ("brake",               DataTypes.FLOAT),         # Brake pedal position (0.0 = released, 1.0 = full brake)
        ("fuel",                DataTypes.FLOAT),         # Remaining fuel in litres
        ("gear",                DataTypes.SIGNED_INT),    # Engaged gear: 0 = reverse, 1 = neutral, 2+ = forward gears
        ("rpms",                DataTypes.SIGNED_INT),    # Engine speed in revolutions per minute
        ("steerAngle",          DataTypes.FLOAT),         # Normalised steering angle (−1.0 = full left, +1.0 = full right)
        ("speedKmh",            DataTypes.FLOAT),         # Vehicle speed in km/h
        ("velocity",            DataTypes.FLOAT * 3),     # World-space velocity vector [X, Y, Z] in m/s
        ("accG",                DataTypes.FLOAT * 3),     # Acceleration in G [lateral X, longitudinal Y, vertical Z]
        ("wheelSlip",           DataTypes.FLOAT * 4),     # Tyre slip value per wheel [FL, FR, RL, RR]
        ("wheelLoad",           DataTypes.FLOAT * 4),     # Vertical tyre load in Newtons [FL, FR, RL, RR]
        ("wheelsPressure",      DataTypes.FLOAT * 4),     # Tyre inflation pressure in PSI [FL, FR, RL, RR]
        ("wheelAngularSpeed",   DataTypes.FLOAT * 4),     # Wheel rotational speed in rad/s [FL, FR, RL, RR]
        ("tyreWear",            DataTypes.FLOAT * 4),     # Tyre wear level (0.0 = new, 1.0 = fully worn) [FL, FR, RL, RR]
        ("tyreDirtyLevel",      DataTypes.FLOAT * 4),     # Amount of dirt / debris on each tyre surface [FL, FR, RL, RR]
        ("tyreCoreTemperature", DataTypes.FLOAT * 4),     # Core temperature of each tyre in °C [FL, FR, RL, RR]
        ("camberRAD",           DataTypes.FLOAT * 4),     # Wheel camber angle in radians per corner [FL, FR, RL, RR]
        ("suspensionTravel",    DataTypes.FLOAT * 4),     # Suspension compression travel in metres [FL, FR, RL, RR]
        ("drs",                 DataTypes.FLOAT),         # DRS flap state (0.0 = closed, 1.0 = fully open)
        ("tc",                  DataTypes.FLOAT),         # Traction control cut intensity (0.0 = inactive, 1.0 = maximum)
        ("heading",             DataTypes.FLOAT),         # Vehicle heading relative to world north in radians
        ("pitch",               DataTypes.FLOAT),         # Chassis pitch angle in radians (positive = nose up)
        ("roll",                DataTypes.FLOAT),         # Chassis roll angle in radians (positive = right side down)
        ("cgHeight",            DataTypes.FLOAT),         # Height of the centre of gravity above the ground in metres
        ("carDamage",           DataTypes.FLOAT * 5),     # Damage level per body zone [front, rear, left, right, centre] (0.0–1.0)
        ("numberOfTyresOut",    DataTypes.SIGNED_INT),    # Number of tyres currently outside track limits
        ("pitLimiterOn",        DataTypes.SIGNED_INT),    # Pit-speed limiter active (0 = off, 1 = on)
        ("abs",                 DataTypes.FLOAT),         # ABS intervention intensity (0.0 = inactive, 1.0 = fully active)
        ("kersCharge",          DataTypes.FLOAT),         # KERS/ERS battery state of charge (0.0–1.0)
        ("kersInput",           DataTypes.FLOAT),         # KERS/ERS power delivery level currently being deployed (0.0–1.0)
        ("autoShifterOn",       DataTypes.SIGNED_INT),    # Automatic gearshift aid active (0 = manual, 1 = auto)
        ("rideHeight",          DataTypes.FLOAT * 2),     # Ride height at front and rear axle in metres [front, rear]
        ("turboBoost",          DataTypes.FLOAT),         # Current turbo boost pressure in bar
        ("ballast",             DataTypes.FLOAT),         # Additional ballast added to the car in kg
        ("airDensity",          DataTypes.FLOAT),         # Ambient air density in kg/m³
        ("airTemp",             DataTypes.FLOAT),         # Ambient air temperature in °C
        ("roadTemp",            DataTypes.FLOAT),         # Road surface temperature in °C
        
        ("localAngularVel",     DataTypes.FLOAT * 3),     # Angular velocity in the car's local frame [pitch, yaw, roll] in rad/s
        ("finalFF",             DataTypes.FLOAT),         # Final force-feedback torque value sent to the wheel (Nm)
        ("performanceMeter",    DataTypes.FLOAT),         # Real-time delta vs. best lap (positive = ahead of reference)
        ("engineBrake",         DataTypes.SIGNED_INT),    # Engine-braking setting level (higher = more engine braking)
        ("ersRecoveryLevel",    DataTypes.SIGNED_INT),    # ERS energy-recovery intensity level
        ("ersPowerLevel",       DataTypes.SIGNED_INT),    # ERS power-deployment level
        ("ersHeatCharging",     DataTypes.SIGNED_INT),    # ERS heat-charging mode active (0 = off, 1 = on)
        ("ersIsCharging",       DataTypes.SIGNED_INT),    # ERS currently recovering energy (0 = deploying, 1 = charging)
        ("kersCurrentKJ",       DataTypes.FLOAT),         # Energy stored in the KERS/ERS battery in kilojoules
        ("drsAvailable",        DataTypes.SIGNED_INT),    # DRS can be activated (0 = no, 1 = yes)
        ("drsEnabled",          DataTypes.SIGNED_INT),    # DRS is open and active (0 = closed, 1 = open)
        ("brakeTemp",           DataTypes.FLOAT * 4),     # Brake disc temperature per corner in °C [FL, FR, RL, RR]
        ("clutch",              DataTypes.FLOAT),         # Clutch pedal position (0.0 = engaged, 1.0 = fully disengaged)
        ("tyreTempI",           DataTypes.FLOAT * 4),     # Tyre inner-edge temperature per wheel in °C [FL, FR, RL, RR]
        ("tyreTempM",           DataTypes.FLOAT * 4),     # Tyre mid-tread temperature per wheel in °C [FL, FR, RL, RR]
        ("tyreTempO",           DataTypes.FLOAT * 4),     # Tyre outer-edge temperature per wheel in °C [FL, FR, RL, RR]
        ("isAIControlled",      DataTypes.SIGNED_INT),    # Car is driven by AI (0 = player, 1 = AI)
        ("tyreContactPoint",    DataTypes.FLOAT * 4 * 3), # 3-D world-space contact point of each tyre with the road [FL,FR,RL,RR][X,Y,Z]
        ("tyreContactNormal",   DataTypes.FLOAT * 4 * 3), # Road-surface normal vector at each tyre contact point [FL,FR,RL,RR][X,Y,Z]
        ("tyreContactHeading",  DataTypes.FLOAT * 4 * 3), # Heading vector at each tyre contact point [FL,FR,RL,RR][X,Y,Z]
        ("brakeBias",           DataTypes.FLOAT),         # Front brake-bias ratio (e.g. 0.56 = 56 % front)
        ("localVelocity",       DataTypes.FLOAT * 3),     # Velocity in the car's local reference frame [X, Y, Z] in m/s
        ("P2PActivations",      DataTypes.SIGNED_INT),    # Remaining Push-to-Pass activations 
        ("P2PStatus",           DataTypes.SIGNED_INT),    # Push-to-Pass status (0 = inactive, 1 = active)
        ("currentMaxRpm",       DataTypes.SIGNED_INT),    # Current rev-limiter ceiling in RPM
        ("mz",                  DataTypes.FLOAT * 4),     # Self-aligning tyre torque (Mz) per wheel [FL, FR, RL, RR] in Nm
        ("fx",                  DataTypes.FLOAT * 4),     # Longitudinal tyre force (Fx) per wheel [FL, FR, RL, RR] in N
        ("fy",                  DataTypes.FLOAT * 4),     # Lateral tyre force (Fy) per wheel [FL, FR, RL, RR] in N
        ("slipRatio",           DataTypes.FLOAT * 4),     # Longitudinal slip ratio per tyre [FL, FR, RL, RR]
        ("slipAngle",           DataTypes.FLOAT * 4),     # Lateral slip angle per tyre in radians [FL, FR, RL, RR]
        ("tcinAction",          DataTypes.SIGNED_INT),    # Traction control currently cutting power (0 = no, 1 = yes)
        ("absInAction",         DataTypes.SIGNED_INT),    # ABS currently modulating brakes (0 = no, 1 = yes)
        ("suspensionDamage",    DataTypes.FLOAT * 4),     # Suspension structural damage per corner (0.0–1.0) [FL, FR, RL, RR]
        ("tyreTemp",            DataTypes.FLOAT * 4),     # Representative tyre surface temperature per wheel in °C [FL, FR, RL, RR]
        ("waterTemp",           DataTypes.FLOAT),         # Engine coolant temperature in °C
        ("brakeTorque",         DataTypes.FLOAT * 4),     # Braking torque at each wheel in Nm [FL, FR, RL, RR]
        ("frontBrakeCompound",  DataTypes.SIGNED_INT),    # Front brake-pad compound identifier
        ("rearBrakeCompound",   DataTypes.SIGNED_INT),    # Rear brake-pad compound identifier
        ("padLife",             DataTypes.FLOAT * 4),     # Brake-pad remaining life per corner (0.0–1.0) [FL, FR, RL, RR]
        ("discLife",            DataTypes.FLOAT * 4),     # Brake-disc remaining life per corner (0.0–1.0) [FL, FR, RL, RR]
        ("ignitionOn",          DataTypes.SIGNED_INT),    # Ignition switch state (0 = off, 1 = on)
        
        ("starterEngineOn",     DataTypes.SIGNED_INT),    # Starter motor currently cranking (0 = no, 1 = yes)
        ("isEngineRunning",     DataTypes.SIGNED_INT),    # Engine is running (0 = stopped, 1 = running)
        ("kerbVibration",       DataTypes.FLOAT),         # Vibration intensity transmitted from kerb strikes
        ("slipVibrations",      DataTypes.FLOAT),         # Vibration intensity caused by tyre slip
        ("roadVibrations",      DataTypes.FLOAT),         # Vibration intensity from road surface texture
        ("absVibrations",       DataTypes.FLOAT),         # Vibration intensity generated by ABS pulsing
    ]


# Main HUD and graphics telemetry page. Updated each rendered frame. Contains embedded sub-structs for tyres,
# damage, electronics, timing, and session state.
class SPageFileGraphicEvoData(DataTypes.STRUCTURE):
    # _pack_ = 1
    _enums_: dict[type, tuple[str, ...]] = {
        ACEVO_STATUS: ("status",),
        ACEVO_CAR_LOCATION: ("car_location",),
        ACEVO_FLAG_TYPE: ("flag", "global_flag",),
        ACEVO_ENGINE_TYPE: ("flag",),
    }
    _fields_ = [
        ("packetId",                            DataTypes.SIGNED_INT),		# Incrementing counter — detect new frames by comparing to previous value
        ("status",                              DataTypes.SIGNED_INT),		# Current simulator operational state (see ACEVO_STATUS)
        ("focused_car_id_a",                    DataTypes.UNSIGNED_INT64),	# Unique ID of the car currently shown by the camera
        ("focused_car_id_b",                    DataTypes.UNSIGNED_INT64),
        ("player_car_id_a",                     DataTypes.UNSIGNED_INT64),	# Unique ID of the player's own car
        ("player_car_id_b",                     DataTypes.UNSIGNED_INT64),
        ("rpm",                                 DataTypes.UNSIGNED_SHORT),	# Engine speed in RPM for HUD display
        ("is_rpm_limiter_on",                   DataTypes.BOOL),			# Rev limiter is cutting fuel / ignition (bouncing off limiter)
        ("is_change_up_rpm",                    DataTypes.BOOL),			# Engine RPM is in the upshift window
        ("is_change_down_rpm",                  DataTypes.BOOL),			# Engine RPM is in the downshift window
        ("tc_active",                           DataTypes.BOOL),			# Traction control is actively intervening this frame
        ("abs_active",                          DataTypes.BOOL),			# ABS is actively modulating brake pressure this frame
        ("esc_active",                          DataTypes.BOOL),			# Electronic stability control is intervening this frame
        ("launch_active",                       DataTypes.BOOL),			# Launch control system is engaged
        ("is_ignition_on",                      DataTypes.BOOL),			# Ignition switch is on
        ("is_engine_running",                   DataTypes.BOOL),			# Engine is running
        ("kers_is_charging",                    DataTypes.BOOL),			# KERS/ERS battery is currently being charged
        ("is_wrong_way",                        DataTypes.BOOL),			# Car is travelling in the wrong direction on track
        ("is_drs_available",                    DataTypes.BOOL),			# DRS activation is permitted in this section
        ("battery_is_charging",                 DataTypes.BOOL),			# High-voltage battery pack is in charging state
        ("is_max_kj_per_lap_reached",           DataTypes.BOOL),			# Maximum ERS deployment energy for this lap has been consumed
        ("is_max_charge_kj_per_lap_reached",    DataTypes.BOOL),			# Maximum ERS charge energy for this lap has been stored
        ("display_speed_kmh",                   DataTypes.SIGNED_SHORT),	# Displayed speed in km/h
        ("display_speed_mph",                   DataTypes.SIGNED_SHORT),	# Displayed speed in mph
        ("display_speed_ms",                    DataTypes.SIGNED_SHORT),	# Displayed speed in m/s
        ("pitspeeding_delta",                   DataTypes.FLOAT),			# Speed delta vs. pit-lane limit (negative = under limit)
        ("gear_int",                            DataTypes.SIGNED_SHORT),	# Current gear as an integer (same encoding as physics gear)
        ("rpm_percent",                         DataTypes.FLOAT),			# Engine RPM as a fraction of redline (0.0–1.0)
        ("gas_percent",                         DataTypes.FLOAT),			# Throttle pedal position as a fraction (0.0–1.0)
        ("brake_percent",                       DataTypes.FLOAT),			# Brake pressure as a fraction (0.0–1.0)
        ("handbrake_percent",                   DataTypes.FLOAT),			# Handbrake engagement as a fraction (0.0–1.0)
        ("clutch_percent",                      DataTypes.FLOAT),			# Clutch disengagement as a fraction (1.0–0.0)
        ("steering_percent",                    DataTypes.FLOAT),			# Steering wheel position (−1.0 = full left, +1.0 = full right)
        ("ffb_strength",                        DataTypes.FLOAT),			# Global force-feedback output strength
        ("car_ffb_mupliplier",                  DataTypes.FLOAT),			# Per-car force-feedback gain multiplier
        ("water_temperature_percent",           DataTypes.FLOAT),			# Coolant temperature as a fraction of optimal operating range
        
        ("water_pressure_bar",					DataTypes.FLOAT),			# Coolant system pressure in bar
        ("fuel_pressure_bar",                   DataTypes.FLOAT),			# Fuel system pressure in bar
        ("water_temperature_c",                 DataTypes.SIGNED_INT8),		# Coolant temperature in °C
        ("air_temperature_c",                   DataTypes.SIGNED_INT8),		# Ambient air temperature in °C
        ("oil_temperature_c",                   DataTypes.FLOAT),			# Engine oil temperature in °C
        ("oil_pressure_bar",                    DataTypes.FLOAT),			# Engine oil pressure in bar
        ("exhaust_temperature_c",               DataTypes.FLOAT),			# Exhaust gas temperature in °C
        ("g_forces_x",                          DataTypes.FLOAT),			# Lateral G-force (positive = rightward)
        ("g_forces_y",                          DataTypes.FLOAT),			# Longitudinal G-force (positive = under acceleration)
        ("g_forces_z",                          DataTypes.FLOAT),			# Vertical G-force (positive = upward)
        ("turbo_boost",                         DataTypes.FLOAT),			# Absolute turbo boost pressure in bar
        ("turbo_boost_level",                   DataTypes.FLOAT),			# Current boost stage or map level
        ("turbo_boost_perc",                    DataTypes.FLOAT),			# Turbo boost as a fraction of maximum (0.0–1.0)
        ("steer_degrees",                       DataTypes.SIGNED_INT32),	# Steering wheel rotation in degrees from centre
        ("current_km",                          DataTypes.FLOAT),			# Distance driven in the current session in km
        ("total_km",                            DataTypes.UNSIGNED_INT32),	# Total odometer / career distance in km
        ("total_driving_time_s",                DataTypes.UNSIGNED_INT32),	# Total driving time accumulated in seconds
        ("time_of_day_hours",                   DataTypes.SIGNED_INT32),	# In-game time of day — hours (0–23)
        ("time_of_day_minutes",                 DataTypes.SIGNED_INT32),	# In-game time of day — minutes (0–59)
        ("time_of_day_seconds",                 DataTypes.SIGNED_INT32),	# In-game time of day — seconds (0–59)
        ("delta_time_ms",                       DataTypes.SIGNED_INT32),	# Delta vs. reference lap in milliseconds (signed)
        ("current_lap_time_ms",                 DataTypes.SIGNED_INT32),	# Current lap time in milliseconds
        ("predicted_lap_time_ms",               DataTypes.SIGNED_INT32),	# Predicted final lap time in milliseconds
        ("fuel_liter_current_quantity",         DataTypes.FLOAT),			# Fuel remaining in the tank in litres
        ("fuel_liter_current_quantity_percent", DataTypes.FLOAT),			# Fuel remaining as a fraction of tank capacity
        ("fuel_liter_per_km",                   DataTypes.FLOAT),			# Average fuel consumption rate in litres per km
        ("km_per_fuel_liter",                   DataTypes.FLOAT),			# Average fuel economy in km per litre
        ("current_torque",                      DataTypes.FLOAT),			# Engine output torque in Nm
        ("current_bhp",                         DataTypes.SIGNED_INT32),	# Engine output power in brake horsepower
        ("tyre_lf",                             SMEvoTyreState),			# Full tyre state for the front-left corner
        ("tyre_rf",                             SMEvoTyreState),			# Full tyre state for the front-right corner
        ("tyre_lr",                             SMEvoTyreState),			# Full tyre state for the rear-left corner
        ("tyre_rr",                             SMEvoTyreState),			# Full tyre state for the rear-right corner
        ("npos",                                DataTypes.FLOAT),			# Normalised track position (0.0 = start/finish line, 1.0 = one full lap)
        ("kers_charge_perc",                    DataTypes.FLOAT),			# KERS/ERS charge level as a fraction (0.0–1.0)
        ("kers_current_perc",                   DataTypes.FLOAT),			# KERS/ERS power currently being deployed as a fraction
        ("control_lock_time",                   DataTypes.FLOAT),			# Seconds driver input remains locked (e.g. after collision penalty)
        ("car_damage",                          SMEvoDamageState),			# Damage levels for each body zone of the car
        ("car_location",                        DataTypes.SIGNED_INT),		# Current track zone the car occupies (see ACEVO_CAR_LOCATION)
        
        ("pit_info",                        SMEvoPitInfo),				# Status of each pit-stop service item
        ("fuel_liter_used",                 DataTypes.FLOAT),			# Fuel consumed since session start in litres
        ("fuel_liter_per_lap",              DataTypes.FLOAT),			# Average fuel consumed per lap in litres
        ("laps_possible_with_fuel",         DataTypes.FLOAT),			# Estimated number of laps achievable with remaining fuel
        ("battery_temperature",             DataTypes.FLOAT),			# High-voltage battery temperature in °C
        ("battery_voltage",                 DataTypes.FLOAT),			# High-voltage battery pack voltage in V
        ("instantaneous_fuel_liter_per_km", DataTypes.FLOAT),			# Instantaneous fuel consumption in litres per km
        ("instantaneous_km_per_fuel_liter", DataTypes.FLOAT),			# Instantaneous fuel economy in km per litre
        ("gear_rpm_window",                 DataTypes.FLOAT),			# How well current RPM suits the engaged gear (1.0 = ideal window)
        ("instrumentation",                 SMEvoInstrumentation),		# Current state of all cockpit lights and displays
        ("instrumentation_min_limit",       SMEvoInstrumentation),		# Minimum allowed setting for each instrumentation item
        ("instrumentation_max_limit",       SMEvoInstrumentation),		# Maximum allowed setting for each instrumentation item
        ("electronics",                     SMEvoElectronics),			# Current electronic aid and setup values
        ("electronics_min_limit",           SMEvoElectronics),			# Minimum allowed value for each electronics setting
        ("electronics_max_limit",           SMEvoElectronics),			# Maximum allowed value for each electronics setting
        ("electronics_is_modifiable",       SMEvoElectronics),			# Flags which electronics fields the driver can adjust in-session
        ("total_lap_count",                 DataTypes.SIGNED_INT32),	# Total laps completed in the session
        ("current_pos",                     DataTypes.UNSIGNED_INT32),	# Current race position (1 = leader)
        ("total_drivers",                   DataTypes.UNSIGNED_INT32),	# Total number of cars in the session
        ("last_laptime_ms",                 DataTypes.SIGNED_INT32),	# Last completed lap time in milliseconds
        ("best_laptime_ms",                 DataTypes.SIGNED_INT32),	# Personal best lap time in milliseconds
        ("flag",                            DataTypes.SIGNED_INT),		# Flag shown specifically to this driver
        ("global_flag",                     DataTypes.SIGNED_INT),		# Flag shown to all drivers on track
        ("max_gears",                       DataTypes.UNSIGNED_INT32),	# Number of forward gears the car has
        ("engine_type",                     DataTypes.SIGNED_INT),		# Powertrain type of the car (see ACEVO_ENGINE_TYPE)
        ("has_kers",                        DataTypes.BOOL),			# Car is equipped with a KERS/ERS system
        ("is_last_lap",                     DataTypes.BOOL),			# This is the final scheduled lap of the race
        ("performance_mode_name",           DataTypes.CHAR * 33),		# Display name of the active vehicle performance / power mode
        ("diff_coast_raw_value",            DataTypes.FLOAT),			# Raw differential coast-lock value from setup
        ("diff_power_raw_value",            DataTypes.FLOAT),			# Raw differential power-lock value from setup
        ("race_cut_gained_time_ms",         DataTypes.SIGNED_INT32),	# Cumulative time penalty from track-limit cuts in ms
        ("distance_to_deadline",            DataTypes.SIGNED_INT32),	# Distance to the penalty trigger in metres
        ("race_cut_current_delta",          DataTypes.FLOAT),			# Running delta time accrued from track-limit violations
        ("session_state",                   SMEvoSessionState),			# Session lifecycle and countdown information
        ("timing_state",                    SMEvoTimingState),			# HUD lap times and delta display values
        ("player_ping",                     DataTypes.SIGNED_INT32),	# Network round-trip ping to the server in ms
        ("player_latency",                  DataTypes.SIGNED_INT32),	# Measured network latency in ms
        ("player_cpu_usage",                DataTypes.SIGNED_INT32),	# Client CPU usage in percent
        ("player_cpu_usage_avg",            DataTypes.SIGNED_INT32),	# Average client CPU usage in percent
        
        ("player_qos",          DataTypes.SIGNED_INT32),	# Network Quality-of-Service score
        ("player_qos_avg",      DataTypes.SIGNED_INT32),	# Average QoS score over the session
        ("player_fps",          DataTypes.SIGNED_INT32),	# Current rendered frames per second
        ("player_fps_avg",      DataTypes.SIGNED_INT32),	# Average FPS over the session
        ("driver_name",         DataTypes.CHAR * 33),		# Driver's first name
        ("driver_surname",      DataTypes.CHAR * 33),		# Driver's surname
        ("car_model",           DataTypes.CHAR * 33),		# Identifier or display name of the car model
        ("is_in_pit_box",       DataTypes.BOOL),			# Car is stationary inside its assigned pit box
        ("is_in_pit_lane",      DataTypes.BOOL),			# Car is anywhere within the pit lane
        ("is_valid_lap",        DataTypes.BOOL),			# Current lap is valid and counts for timing
        ("car_coordinates",     DataTypes.FLOAT * 60 * 3),	# World-space position of up to 60 cars [car_index][X, Y, Z]
        ("gap_ahead",           DataTypes.FLOAT),			# Time gap to the car immediately ahead in seconds
        ("gap_behind",          DataTypes.FLOAT),			# Time gap to the car immediately behind in seconds
        ("active_cars",         DataTypes.UNSIGNED_INT8),	# Number of cars actively participating in the session
        ("fuel_per_lap",        DataTypes.FLOAT),			# Target fuel consumption per lap in litres
        ("fuel_estimated_laps", DataTypes.FLOAT),			# Estimated laps remaining with current fuel
        ("assists_state",       SMEvoAssistsState),			# All driver-assist levels currently active
        ("max_fuel",            DataTypes.FLOAT),			# Maximum fuel tank capacity of the car in litres
        ("max_turbo_boost",     DataTypes.FLOAT),			# Maximum turbo boost pressure in bar
        ("use_single_compound", DataTypes.BOOL),			# Car is restricted to a single tyre compound for both axles
        ("car_ids",             DataTypes.UNSIGNED_INT64),	# Car UID mapping for indexing car_coordinates
    ]


# Static session metadata. Written once when a session loads and does not change while driving.
class SPageFileStaticEvoData(DataTypes.STRUCTURE):
    # _pack_ = 1
    _enums_: dict[type, tuple[str, ...]] = {
        ACEVO_SESSION_TYPE: ("session",),
        ACEVO_STARTING_GRIP: ("starting_grip",),
    }
    _fields_ = [
        ("sm_version",                      DataTypes.CHAR * 15),		# Shared-memory interface version string
        ("ac_evo_version",                  DataTypes.CHAR * 15),		# AC Evo game build version string
        ("session",                         DataTypes.SIGNED_INT),		# Type of the current session (see ACEVO_SESSION_TYPE)
        ("session_name",                    DataTypes.CHAR * 33),		# Human-readable session name (e.g. 'Race 1')
        ("event_id",                        DataTypes.UNSIGNED_INT8),	# Unique identifier of the event within the championship
        ("session_id",                      DataTypes.UNSIGNED_INT8),	# Unique identifier of this session within the event
        ("starting_grip",                   DataTypes.SIGNED_INT),		# Tyre grip condition at session start (see ACEVO_STARTING_GRIP)
        ("starting_ambient_temperature_c",  DataTypes.FLOAT),			# Ambient air temperature at session start in °C
        ("starting_ground_temperature_c",   DataTypes.FLOAT),			# Road surface temperature at session start in °C
        ("is_static_weather",               DataTypes.BOOL),			# Weather is fixed and will not change during the session
        ("is_timed_race",                   DataTypes.BOOL),			# Session ends by elapsed time rather than lap count
        ("is_online",                       DataTypes.BOOL),			# Session is an online multiplayer event
        ("number_of_sessions",              DataTypes.SIGNED_INT),		# Total sessions in this event (e.g. 3 = practice + qualify + race)
        ("nation",                          DataTypes.CHAR * 33),		# Country / nation name associated with the event or track
        ("longitude",                       DataTypes.FLOAT),			# Geographic longitude of the track location in decimal degree
        ("latitude",                        DataTypes.FLOAT),			# Geographic latitude of the track location in decimal degrees
        ("track",                           DataTypes.CHAR * 33),		# Track identifier or name
        ("track_configuration",             DataTypes.CHAR * 33),		# Track layout variant or configuration name
        ("track_length_m",                  DataTypes.FLOAT),			# Total lap length of the track in metres
    ]


### * MetaData

class MetaData:
    # standard network info
    port: int | None = None
    
    # use if a heartbeat is needed
    heartBeatPort: int | None = None
    heartBeatFunc = None
    
    # use for itinial hand shake
    handShakePort: int | None = None
    handShakeFunc: tuple | None = None
    
    # use if the data needs decrypting
    decrytionFunc = None
    
    # use if there is a header packet
    headerInfo: type | None = None
    packetIDAttribute: str | None = None
    
    # use for shared memory
    allSharedMemoryNames: str | None | dict[str, str] = {
            "SPageFilePhysicsData": "Local\\acevo_pmf_physics",
            "SPageFileGraphicEvoData": "Local\\acevo_pmf_graphics",
            "SPageFileStaticEvoData": "Local\\acevo_pmf_static",
        }
    
    # standard packet info
    packetInfo: dict[int, tuple[type, ...]] = {
        0: (SPageFilePhysicsData, SPageFileGraphicEvoData, SPageFileStaticEvoData,),
    }