import ctypes
from enum import Enum, IntEnum, StrEnum


class DataTypes:
    STRUCTURE = ctypes.LittleEndianStructure
    UNION = ctypes.Union
    
    SIGNED_INT8 = ctypes.c_int8
    SIGNED_INT16 = ctypes.c_int16
    # SIGNED_INT32 = ctypes.c_int32
    
    UNSIGNED_INT8 = ctypes.c_uint8
    UNSIGNED_INT16 = ctypes.c_uint16
    UNSIGNED_INT32 = ctypes.c_uint32
    UNSIGNED_INT64 = ctypes.c_uint64
    
    FLOAT = ctypes.c_float
    CHAR = ctypes.c_char
    DOUBLE = ctypes.c_double


### * Enums

class PACKET_ID(IntEnum):
    Motion = 0
    Session = 1
    LapData = 2
    Event = 3
    Participants = 4
    CarSetups = 5
    CarTelemetry = 6
    CarStatus = 7
    FinalClassification = 8
    LobbyInfo = 9
    CarDamage = 10
    SessionHistory = 11

class TEAM_ID(IntEnum):
    Mercedes = 0
    Ferrari = 1
    Red_Bull_Racing = 2
    Williams = 3
    Aston_Martin = 4
    Alpine = 5
    Alpha_Tauri = 6
    Haas = 7
    McLaren = 8
    Alfa_Romeo = 9
    # McLaren_1988 = 10
    # McLaren_1991 = 11
    # Williams_1992 = 12
    # Ferrari_1995 = 13
    # Williams_1996 = 14
    # McLaren_1998 = 15
    # Ferrari_2002 = 16
    # Ferrari_2004 = 17
    # Renault_2006 = 18
    # Ferrari_2007 = 19
    # McLaren_2008 = 20
    # Redbull_2010 = 21
    # Ferrari_1976 = 22
    # ART_Grand_Prix = 23
    # Campos_Vexatec_Racing = 24
    # Carlin = 25
    # Charouz_Racing_System = 26
    # DAMS = 27
    # Russian_Time = 28
    # MP_Motorsport = 29
    # Pertamina = 30
    # McLaren_1990 = 31
    # Trident = 32
    # BWT_Arden = 33
    # McLaren_1976 = 34
    # Lotus_1972 = 35
    # Ferrari_1979 = 36
    # McLaren_1982 = 37
    # Williams_2003 = 38
    # Brawn_2009 = 39
    # Lotus_1978 = 40
    # F1_Generic_Car = 41
    ART_GP_19 = 42
    Campos_19 = 43
    Carlin_19 = 44
    Sauber_Junior_Charouz_19 = 45
    Dams_19 = 46
    Uni_Virtuosi_19 = 47
    MP_Motorsport_19 = 48
    Prema_19 = 49
    Trident_19 = 50
    Arden_19 = 51
    # Benetton_1994 = 53
    # Benetton_1995 = 54
    # Ferrari_2000 = 55
    # Jordan_1991 = 56
    # Ferrri_1990 = 63
    # McLaren_2010 = 64
    # Ferrari_2010 = 65
    Art_GP_20 = 70
    Campos_20 = 71
    Carlin_20 = 72
    Charouz_20 = 73
    Dams_20 = 74
    Uni_Virtuosi_20 = 75
    MP_Motorsport_20 = 76
    Prema_20 = 77
    Trident_20 = 78
    BWT_20 = 79
    Hitech_20 = 80
    Mercedes_2020 = 85
    Ferrari_2020 = 86
    Red_Bull_2020 = 87
    Williams_2020 = 88
    Racing_Point_2020 = 89
    Renault_2020 = 90
    Alpha_Tauri_2020 = 91
    Haas_2020 = 92
    McLaren_2020 = 93
    Alfa_Romeo_2020 = 84
    # My_Team = 255

class DRIVER_ID(IntEnum):
    Carlos_Sainz = 0
    Daniil_Kvyat = 1
    Daniel_Ricciardo = 2
    Fernando_Alonso = 3
    Felipe_Massa = 4
    Kimi_Räikkönen = 6
    Lewis_Hamilton = 7
    # Marcus_Ericsson = 8
    Max_Verstappen = 9
    Nico_Hulkenberg = 10
    Kevin_Magnussen = 11
    Romain_Grosjean = 12
    Sebastian_Vettel = 13
    Sergio_Perez = 14
    Valtteri_Bottas = 15
    Esteban_Ocon = 17
    # Stoffel_Vandoorne = 18
    Lance_Stroll = 19
    Arron_Barnes = 20
    Martin_Giles = 21
    Alex_Murray = 22
    Lucas_Roth = 23
    Igor_Correia = 24
    Sophie_Levasseur = 25
    Jonas_Schiffer = 26
    Alain_Forest = 27
    Jay_Letourneau = 28
    Esto_Saari = 29
    Yasar_Atiyeh = 30
    Callisto_Calabresi = 31
    Naota_Izum = 32
    Howard_Clarke = 33
    Wilheim_KaufMann = 34
    Marie_Laursen = 35
    Flavio_Nieves = 36
    Peter_Belousov = 37
    Klimek_Michalski = 38
    Santiago_Moreno = 39
    Benjamin_Coppens = 40
    Noah_Visser = 41
    Gert_Waldmuller = 42
    Julian_Quesada = 43
    Daniel_Jones = 44
    Artem_Markelov = 45
    Tadasuke_Makino = 46
    Sean_Gelael = 47
    Nyck_De_Vries = 48
    Jack_Aitken = 49
    George_Russell = 50
    Maximilian_Günther = 51
    Nirei_Fukuzumi = 52
    Luca_Ghiotto = 53
    Lando_Norris = 54
    Sérgio_Sette_Câmara = 55
    Louis_Delétraz = 56
    Antonio_Fuoco = 57
    Charles_Leclerc = 58
    Pierre_Gasly = 59
    # Brendon_Hartley = 60
    # Sergey_Sirotkin = 61
    Alexander_Albon = 62
    Nicholas_Latifi = 63
    Dorlan_Boccolacci = 64
    Niko_Kari = 65
    Roberto_Merhi = 66
    Arjun_Maini = 67
    Alessio_Lorandi = 68
    Ruben_Meijer = 69
    Rashid_Nair = 70
    Jack_Tremblay = 71
    Devon_Butler = 72
    Lukas_Weber = 73
    Antonio_Giovinazzi = 74
    Robert_Kubica = 75
    Alain_Prost = 76
    Ayrton_Senna = 77
    Nobuharu_Matsushita = 78
    Nikita_Mazepin = 79
    Guanya_Zhou = 80
    Mick_Schumacher = 81
    Callum_Ilott = 82
    Juan_Manuel_Correa = 83
    Jordan_King = 84
    Mahaveer_Raghunathan = 85
    Tatiana_Calderon = 86
    Anthoine_Hubert = 87
    Guiliano_Alesi = 88
    Ralph_Boschung = 89
    Micheal_Schumacher = 90
    Dan_Ticktum = 91
    Marcus_Armstrong = 92
    Christian_Lundgaard = 93
    Yuki_Tsunoda = 94
    Jehan_Daruvala = 95
    Gulherme_Samaia = 96
    Pedro_Piquet = 97
    Felipe_Drugovich = 98
    Robert_Schwartzman = 99
    Roy_Nissany = 100
    Marino_Sato = 101
    Aidan_Jackson = 102
    Casper_Akkerman = 103
    Jenson_Button = 109
    David_Coulthard = 110
    Nico_Rosberg = 111

class TRACK_ID(IntEnum):
    Unknown = -1
    Melbourne = 0
    Paul_Ricard = 1
    Shanghai = 2
    Sakhir_Bahrain = 3
    Catalunya = 4
    Monaco = 5
    Montreal = 6
    Silverstone = 7
    Hockenheim = 8
    Hungaroring = 9
    Spa = 10
    Monza = 11
    Singapore = 12
    Suzuka = 13
    Abu_Dhabi = 14
    Texas = 15
    Brazil = 16
    Austria = 17
    Sochi = 18
    Mexico = 19
    Baka_Azerbaijan = 20
    Sakhir_Short = 21
    Silverstone_Short = 22
    Texas_Short = 23
    Suzuka_Short = 24
    Hanoi = 25
    Zandvoort = 26
    Imola = 27
    Portimão = 28
    Jeddah = 29

class NATIONALITY_ID(IntEnum):
    American = 1
    Argentinean = 2
    Australian = 3
    Austrian = 4
    Azerbaijani = 5
    Bahraini = 6
    Belgian = 7
    Bolivian = 8
    Brazilian = 9
    British = 10
    Bulgarian = 11
    Cameroonian = 12
    Canadian = 13
    Chilaen = 14
    Chinese = 15
    Colombian = 16
    Costa_Rican = 17
    Croatian = 18
    Cypriot = 19
    Czech = 20
    Danish = 21
    Dutch = 22
    Ecuadorian = 23
    English = 24
    Emirian = 25
    Estonia = 26
    Finnish = 27
    French = 28
    German = 29
    Ghanaian = 30
    Greek = 31
    Guatemalan = 32
    Honduran = 33
    Hong_Konger = 34
    Hungarian = 35
    Icelander = 36
    Indian = 37
    Indonesian = 38
    Irish = 39
    Israeli = 40
    Italian = 41
    Jamaican = 42
    Japanese = 43
    Jordanian = 44
    Kuwaiti = 45
    Latvian = 46
    Lebanese = 47
    Lithuanian = 48
    Luxembourger = 49
    Malaysian = 50
    Maltese = 51
    Mexian = 52
    Monegasque = 53
    New_Zealander = 54
    Nicaraguan = 55
    Northen_Irish = 56
    Norwegian = 57
    Omani = 58
    Pakistani = 59
    Panamanian = 60
    Paraguayan = 61
    Peruvian = 62
    Polish = 63
    Portuguese = 64
    Qatari = 65
    Romanian = 66
    Russian = 67
    Salvadoran = 68
    Saudi = 69
    Scottish = 70
    Serbian = 71
    Singaporean = 72
    Slovakian = 73
    Slovenian = 74
    South_Korean = 75
    South_African = 76
    Spanish = 77
    Swedish = 78
    Swiss = 79
    Thai = 80
    Turkish = 81
    Uruguayan = 82
    Ukrainian = 83
    Venezuelan = 84
    Barbadian = 85
    Welsh = 86
    Vietnamese = 87

class EVENT_STRING_CODE(StrEnum):
    Session_Started = "SSTA"
    Session_Ended = "SEND"
    Fastest_Lap = "FTLP"
    Retirement = "RTMT"
    DRS_Enabled = "DRSE"
    DRS_Disabled = "DRSD"
    Team_Mate_In_Pits = "TMPT"
    Chequered_Flag = "CHQF"
    Race_Winner = "RCWN"
    Penalty_Issued = "PENA"
    Speed_Trap_Triggered = "SPTP"
    Start_Lights = "STLG"
    Lights_Out = "LGOT"
    Drive_Through_Served = "DTSV"
    Stop_Go_Served = "SGSV"
    Flashback = "FLBK"
    Button_status = "BUTN"

class SURFACE_TYPE(IntEnum):
    Tarmac = 0
    Rumble_Strip = 1
    Concrete = 2
    Rock = 3
    Gravel = 4
    Mud = 5
    Sand = 6
    Grass = 7
    Water = 8
    Cobblestone = 9
    Metal = 10
    Ridged = 11

class PENALTY_TYPE(IntEnum):
    Drive_Through = 0
    Stop_Go = 1
    Grid_Penalty = 2
    Penalty_Reminder = 3
    Time_Penalty = 4
    Warning = 5
    Disqualied = 6
    Removed_From_Formation_Lap = 7
    Parked_Too_Long_Timer = 8
    Tyre_Regulations = 9
    This_Lap_Invalidated = 10
    This_And_Next_Lap_Invalidated = 11
    This_Lap_Invalidated_Without_Reason = 12
    This_And_Next_Lap_Invalidated_Without_Reason = 13
    This_And_Previous_Lap_Invalidated = 14
    This_And_Previous_Lap_Invalidated_Without_Reason = 15
    Retired = 16
    Black_Flag_Timer = 17

class INFRINGEMENT_TYPE(IntEnum):
    Blocking_by_slow_driving = 0
    Blocking_by_wrong_way_driving = 1
    Reversing_off_the_start_line = 2
    Big_Collision = 3
    Small_Collision = 4
    Collision_failed_to_hand_back_position_single = 5
    Collision_failed_to_hand_back_position_multiple = 6
    Corner_cutting_gained_time = 7
    Corner_cutting_overtake_single = 8
    Corner_cutting_overtake_multiple = 9
    Crossed_pit_exit_lane = 10
    Ignoring_blue_flags = 11
    Ignoring_yellow_flags = 12
    Ignoring_drive_through = 13
    Too_many_drive_throughs = 14
    Drive_through_reminder_serve_within_n_laps = 15
    Drive_through_reminder_serve_this_lap = 16
    Pit_lane_speeding = 17
    Parked_for_too_long = 18
    Ignoring_tyre_regulations = 19
    Too_many_penalties = 20
    Multiple_warnings = 21
    Approaching_disqualification = 22
    Tyre_regulations_select_single = 23
    Tyre_regulations_select_multiple = 24
    Lap_invalidated_corner_cutting = 25
    Lap_invalidated_running_wide = 26
    Corner_cutting_ran_wide_gained_time_minor = 27
    Corner_cutting_ran_wide_gained_time_significant = 28
    Corner_cutting_ran_wide_gained_time_extreme = 29
    Lap_invalidated_wall_riding = 30
    Lap_invalidated_flashback_used = 31
    Lap_invalidated_reset_to_track = 32
    Blocking_the_pitlane = 33
    Jump_start = 34
    Safety_car_to_car_collision = 35
    Safety_car_illegal_overtake = 36
    Safety_car_exceeding_allowed_pace = 37
    Virtual_safety_car_exceeding_allowed_pace = 38
    Formation_lap_below_allowed_speed = 39
    Retired_mechanical_failure = 40
    Retired_terminally_damaged = 41
    Safety_car_falling_too_far_back = 42
    Black_flag_timer = 43
    Unserved_stop_go_penalty = 44
    Unserved_drive_through_penalty = 45
    Engine_component_change = 46
    Gearbox_change = 47
    League_grid_penalty = 48
    Retry_penalty = 49
    Illegal_time_gain = 50
    Mandatory_pitstop = 51


### * Data Structure

### Packet Header -- 27 bytes

class PacketHeader(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _enums_: dict[type, tuple[str, ...]] = {
        PACKET_ID: ("m_packetId",),
    }
    _fields_ = [
        ("m_packetFormat",              DataTypes.UNSIGNED_INT16),    # 2021
        ("m_gameMajorVersion",          DataTypes.UNSIGNED_INT8),     # Game major version - "X.00"
        ("m_gameMinorVersion",          DataTypes.UNSIGNED_INT8),     # Game minor version - "1.XX"
        ("m_packetVersion",             DataTypes.UNSIGNED_INT8),     # Version of this packet type, all start from 1
        ("m_packetId",                  DataTypes.UNSIGNED_INT8),     # Identifier for the packet type, see below
        ("m_sessionUID",                DataTypes.UNSIGNED_INT64),    # Unique identifier for the session
        ("m_sessionTime",               DataTypes.FLOAT),             # Session timestamp
        ("m_frameIdentifier",           DataTypes.UNSIGNED_INT32),    # Identifier for the frame the data was retrieved on
        ("m_playerCarIndex",            DataTypes.UNSIGNED_INT8),     # Index of player's car in the array
        ("m_secondaryPlayerCarIndex",   DataTypes.UNSIGNED_INT8),     # Index of secondary player's car in the array (splitscreen), 255 if no second player
    ]


### Motion Packet -- Rate as specified in menus -- 1464 bytes

class CarMotionData(DataTypes.STRUCTURE):
    # _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_worldPositionX",        DataTypes.FLOAT),         # World space X position
        ("m_worldPositionY",        DataTypes.FLOAT),         # World space Y position
        ("m_worldPositionZ",        DataTypes.FLOAT),         # World space Z position
        ("m_worldVelocityX",        DataTypes.FLOAT),         # Velocity in world space X
        ("m_worldVelocityY",        DataTypes.FLOAT),         # Velocity in world space Y
        ("m_worldVelocityZ",        DataTypes.FLOAT),         # Velocity in world space Z
        ("m_worldForwardDirX",      DataTypes.SIGNED_INT16),  # World space forward X direction (normalised)
        ("m_worldForwardDirY",      DataTypes.SIGNED_INT16),  # World space forward Y direction (normalised)
        ("m_worldForwardDirZ",      DataTypes.SIGNED_INT16),  # World space forward Z direction (normalised)
        ("m_worldRightDirX",        DataTypes.SIGNED_INT16),  # World space right X direction (normalised)
        ("m_worldRightDirY",        DataTypes.SIGNED_INT16),  # World space right Y direction (normalised)
        ("m_worldRightDirZ",        DataTypes.SIGNED_INT16),  # World space right Z direction (normalised)
        ("m_gForceLateral",         DataTypes.FLOAT),         # Lateral G-Force component
        ("m_gForceLongitudinal",    DataTypes.FLOAT),         # Longitudinal G-Force component
        ("m_gForceVertical",        DataTypes.FLOAT),         # Vertical G-Force component
        ("m_yaw",                   DataTypes.FLOAT),         # Yaw angle in radians
        ("m_pitch",                 DataTypes.FLOAT),         # Pitch angle in radians
        ("m_roll",                  DataTypes.FLOAT),         # Roll angle in radians
    ]

class PacketMotionData(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_header",        PacketHeader),          # Header
        ("m_carMotionData", CarMotionData * 22),    # Data for all cars on track
        # Extra player car ONLY data
        ("m_suspensionPosition",        DataTypes.FLOAT * 4),     # Note: All wheel arrays have the following order:
        ("m_suspensionVelocity",        DataTypes.FLOAT * 4),     # RL, RR, FL, FR
        ("m_suspensionAcceleration",    DataTypes.FLOAT * 4),     # RL, RR, FL, FR
        ("m_wheelSpeed",                DataTypes.FLOAT * 4),     # Speed of each wheel
        ("m_wheelSlip",                 DataTypes.FLOAT * 4),     # Slip ratio for each wheel
        ("m_localVelocityX",            DataTypes.FLOAT),         # Velocity in local space
        ("m_localVelocityY",            DataTypes.FLOAT),         # Velocity in local space
        ("m_localVelocityZ",            DataTypes.FLOAT),         # Velocity in local space
        ("m_angularVelocityX",          DataTypes.FLOAT),         # Angular velocity x-component
        ("m_angularVelocityY",          DataTypes.FLOAT),         # Angular velocity y-component
        ("m_angularVelocityZ",          DataTypes.FLOAT),         # Angular velocity z-component
        ("m_angularAccelerationX",      DataTypes.FLOAT),         # Angular acceleration x-component
        ("m_angularAccelerationY",      DataTypes.FLOAT),         # Angular acceleration y-component
        ("m_angularAccelerationZ",      DataTypes.FLOAT),         # Angular acceleration z-component
        ("m_frontWheelsAngle",          DataTypes.FLOAT),         # Current front wheels angle in radians
    ]


### Session Packet -- 2 per second -- 625 bytes

class MarshalZone(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_zoneStart", DataTypes.FLOAT),         # Fraction (0..1) of way through the lap the marshal zone starts
        ("m_zoneFlag",  DataTypes.SIGNED_INT8),   # -1 = invalid/unknown, 0 = none, 1 = green, 2 = blue, 3 = yellow, 4 = red
    ]

class WeatherForecastSample(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_sessionType",               DataTypes.UNSIGNED_INT8), # 0 = unknown, 1 = P1, 2 = P2, 3 = P3, 4 = Short P, 5 = Q1, 6 = Q2, 7 = Q3, 8 = Short Q, 9 = OSQ, 10 = R, 11 = R2, 12 = R3, 13 = Time Trial
        ("m_timeOffset",                DataTypes.UNSIGNED_INT8), # Time in minutes the forecast is for
        ("m_weather",                   DataTypes.UNSIGNED_INT8), # Weather - 0 = clear, 1 = light cloud, 2 = overcast, 3 = light rain, 4 = heavy rain, 5 = storm
        ("m_trackTemperature",          DataTypes.SIGNED_INT8),   # Track temp. in degrees Celsius
        ("m_trackTemperatureChange",    DataTypes.SIGNED_INT8),   # Track temp. change – 0 = up, 1 = down, 2 = no change
        ("m_airTemperature",            DataTypes.SIGNED_INT8),   # Air temp. in degrees celsius
        ("m_airTemperatureChange",      DataTypes.SIGNED_INT8),   # Air temp. change – 0 = up, 1 = down, 2 = no change
        ("m_rainPercentage",            DataTypes.UNSIGNED_INT8), # Rain percentage (0-100)
    ]

class PacketSessionData(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _enums_: dict[type, tuple[str, ...]] = {
        TRACK_ID: ("m_trackId",),
    }
    _fields_ = [
        ("m_header",                            PacketHeader),                          # Header
        ("m_weather",                           DataTypes.UNSIGNED_INT8),         # Weather - 0 = clear, 1 = light cloud, 2 = overcast, 3 = light rain, 4 = heavy rain, 5 = storm
        ("m_trackTemperature",                  DataTypes.SIGNED_INT8),           # Track temp. in degrees celsius
        ("m_airTemperature",                    DataTypes.SIGNED_INT8),           # Air temp. in degrees celsius
        ("m_totalLaps",                         DataTypes.UNSIGNED_INT8),         # Total number of laps in this race
        ("m_trackLength",                       DataTypes.UNSIGNED_INT16),        # Track length in metres
        ("m_sessionType",                       DataTypes.UNSIGNED_INT8),         # 0 = unknown, 1 = P1, 2 = P2, 3 = P3, 4 = Short P, 5 = Q1, 6 = Q2, 7 = Q3, 8 = Short Q, 9 = OSQ, 10 = R, 11 = R2, 12 = R3, 13 = Time Trial
        ("m_trackId",                           DataTypes.SIGNED_INT8),           # -1 for unknown, see appendix
        ("m_formula",                           DataTypes.UNSIGNED_INT8),         # Formula, 0 = F1 Modern, 1 = F1 Classic, 2 = F2, 3 = F1 Generic, 4 = Beta, 5 = Supercars, 6 = Esports, 7 = F2 2021
        ("m_sessionTimeLeft",                   DataTypes.UNSIGNED_INT16),        # Time left in session in seconds
        ("m_sessionDuration",                   DataTypes.UNSIGNED_INT16),        # Session duration in seconds
        ("m_pitSpeedLimit",                     DataTypes.UNSIGNED_INT8),         # Pit speed limit in kilometres per hour
        ("m_gamePaused",                        DataTypes.UNSIGNED_INT8),         # Whether the game is paused – network game only
        ("m_isSpectating",                      DataTypes.UNSIGNED_INT8),         # Whether the player is spectating
        ("m_spectatorCarIndex",                 DataTypes.UNSIGNED_INT8),         # Index of the car being spectated
        ("m_sliProNativeSupport",               DataTypes.UNSIGNED_INT8),         # SLI Pro support, 0 = inactive, 1 = active
        ("m_numMarshalZones",                   DataTypes.UNSIGNED_INT8),         # Number of marshal zones to follow
        ("m_marshalZones",                      MarshalZone * 21),                      # List of marshal zones – max 21
        ("m_safetyCarStatus",                   DataTypes.UNSIGNED_INT8),         # 0 = no safety car, 1 = full, 2 = virtual, 3 = formation lap
        ("m_networkGame",                       DataTypes.UNSIGNED_INT8),         # 0 = offline, 1 = online
        ("m_numWeatherForecastSamples",         DataTypes.UNSIGNED_INT8),         # Number of weather samples to follow
        ("m_weatherForecastSamples",            WeatherForecastSample * 56),            # Array of weather forecast samples
        ("m_forecastAccuracy",                  DataTypes.UNSIGNED_INT8),         # 0 = Perfect, 1 = Approximate
        ("m_aiDifficulty",                      DataTypes.UNSIGNED_INT8),         # AI Difficulty rating – 0-110
        ("m_seasonLinkIdentifier",              DataTypes.UNSIGNED_INT32),        # Identifier for season - persists across saves
        ("m_weekendLinkIdentifier",             DataTypes.UNSIGNED_INT32),        # Identifier for weekend - persists across saves
        ("m_sessionLinkIdentifier",             DataTypes.UNSIGNED_INT32),        # Identifier for session - persists across saves
        ("m_pitStopWindowIdealLap",             DataTypes.UNSIGNED_INT8),         # Ideal lap to pit on for current strategy (player)
        ("m_pitStopWindowLatestLap",            DataTypes.UNSIGNED_INT8),         # Latest lap to pit on for current strategy (player)
        ("m_pitStopRejoinPosition",             DataTypes.UNSIGNED_INT8),         # Predicted position to rejoin at (player)
        ("m_steeringAssist",                    DataTypes.UNSIGNED_INT8),         # 0 = off, 1 = on
        ("m_brakingAssist",                     DataTypes.UNSIGNED_INT8),         # 0 = off, 1 = low, 2 = medium, 3 = high
        ("m_gearboxAssist",                     DataTypes.UNSIGNED_INT8),         # 1 = manual, 2 = manual & suggested gear, 3 = auto
        ("m_pitAssist",                         DataTypes.UNSIGNED_INT8),         # 0 = off, 1 = on
        ("m_pitReleaseAssist",                  DataTypes.UNSIGNED_INT8),         # 0 = off, 1 = on
        ("m_ERSAssist",                         DataTypes.UNSIGNED_INT8),         # 0 = off, 1 = on
        ("m_DRSAssist",                         DataTypes.UNSIGNED_INT8),         # 0 = off, 1 = on
        ("m_dynamicRacingLine",                 DataTypes.UNSIGNED_INT8),         # 0 = off, 1 = corners only, 2 = full
        ("m_dynamicRacingLineType",             DataTypes.UNSIGNED_INT8),         # 0 = 2D, 1 = 3D
    ]


### Lap Data Packet -- Rate as specified in menus -- 970 bytes

class LapData(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_lastLapTimeInMs",               DataTypes.UNSIGNED_INT32),    # Last lap time in milliseconds
        ("m_currentLapTimeInMs",            DataTypes.UNSIGNED_INT32),    # Current time around the lap in milliseconds
        ("m_sector1TimeInMs",               DataTypes.UNSIGNED_INT16),    # Sector 1 time in milliseconds
        ("m_sector2TimeInMs",               DataTypes.UNSIGNED_INT16),    # Sector 2 time in milliseconds
        ("m_lapDistance",                   DataTypes.FLOAT),             # Distance vehicle is around current lap in metres - can, be negative if line not crossed yet
        ("m_totalDistance",                 DataTypes.FLOAT),             # Total distance travelled in session in metres - can, be negative if line not crossed yet
        ("m_safetyCarDelta",                DataTypes.FLOAT),             # Delta in seconds for safety car
        ("m_carPosition",                   DataTypes.UNSIGNED_INT8),     # Car race position
        ("m_currentLapNum",                 DataTypes.UNSIGNED_INT8),     # Current lap number
        ("m_pitStatus",                     DataTypes.UNSIGNED_INT8),     # 0 = none, 1 = pitting, 2 = in pit area
        ("m_numPitStops",                   DataTypes.UNSIGNED_INT8),     # Number of pit stops taken in this race
        ("m_sector",                        DataTypes.UNSIGNED_INT8),     # 0 = sector1, 1 = sector2, 2 = sector3
        ("m_currentLapInvalid",             DataTypes.UNSIGNED_INT8),     # Current lap invalid - 0 = valid, 1 = invalid
        ("m_penalties",                     DataTypes.UNSIGNED_INT8),     # Accumulated time penalties in seconds to be added
        ("m_warnings",                      DataTypes.UNSIGNED_INT8),     # Accumulated number of warnings issued
        ("m_numUnservedDriveThroughPens",   DataTypes.UNSIGNED_INT8),     # Num drive through pens left to serve
        ("m_numUnservedStopGoPens",         DataTypes.UNSIGNED_INT8),     # Num stop go pens left to serve
        ("m_gridPosition",                  DataTypes.UNSIGNED_INT8),     # Grid position the vehicle started the race in
        ("m_driverStatus",                  DataTypes.UNSIGNED_INT8),     # Status of driver - 0 = in garage, 1 = flying lap, 2 = in lap, 3 = out lap, 4 = on track
        ("m_resultStatus",                  DataTypes.UNSIGNED_INT8),     # Result status - 0 = invalid, 1 = inactive, 2 = active, 3 = finished, 4 = didnotfinish, 5 = disqualified, 6 = not classified, 7 = retired
        ("m_pitLaneTimerActive",            DataTypes.UNSIGNED_INT8),     # Pit lane timing, 0 = inactive, 1 = active
        ("m_pitLaneTimeInLaneInMs",         DataTypes.UNSIGNED_INT16),    # If active, the current time spent in the pit lane in ms
        ("m_pitStopTimerInMs",              DataTypes.UNSIGNED_INT16),    # Time of the actual pit stop in ms
        ("m_pitStopShouldServePen",         DataTypes.UNSIGNED_INT8),     # Whether the car should serve a penalty at this stop
    ]

class PacketLapData(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_header",                PacketHeader),                      # Header
        ("m_lapData",               LapData * 22),                      # Lap data for all cars on track
    ]


### Event Packet -- When the event occurs -- 36 bytes

class FastestLap(DataTypes.STRUCTURE):
    _fields_ = [
        ("vehicleIdx",  DataTypes.UNSIGNED_INT8), # Vehicle index of car achieving fastest lap
        ("lapTime",     DataTypes.FLOAT),         # Lap time is in seconds
    ]

class Retirement(DataTypes.STRUCTURE):
    _fields_ = [
        ("vehicleIdx",  DataTypes.UNSIGNED_INT8)  # Vehicle index of car retiring
    ]  

class TeamMateInPits(DataTypes.STRUCTURE):
    _fields_ = [
        ("vehicleIdx",  DataTypes.UNSIGNED_INT8)  # Vehicle index of team mate
    ]  

class RaceWinner(DataTypes.STRUCTURE):
    _fields_ = [
        ("vehicleIdx",  DataTypes.UNSIGNED_INT8)  # Vehicle index of the race winner
    ]  

class Penalty(DataTypes.STRUCTURE):
    _enums_: dict[type, tuple[str, ...]] = {
        PENALTY_TYPE: ("penaltyType",),
        INFRINGEMENT_TYPE: ("infringementType",),
    }
    _fields_ = [
        ("penaltyType",         DataTypes.UNSIGNED_INT8), # Penalty type – see Appendices
        ("infringementType",    DataTypes.UNSIGNED_INT8), # Infringement type – see Appendices
        ("vehicleIdx",          DataTypes.UNSIGNED_INT8), # Vehicle index of the car the penalty is applied to
        ("otherVehicleIdx",     DataTypes.UNSIGNED_INT8), # Vehicle index of the other car involved
        ("time",                DataTypes.UNSIGNED_INT8), # Time gained, or time spent doing action in seconds
        ("lapNum",              DataTypes.UNSIGNED_INT8), # Lap the penalty occurred on
        ("placesGained",        DataTypes.UNSIGNED_INT8), # Number of places gained by this
    ]

class SpeedTrap(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("vehicleIdx",                  DataTypes.UNSIGNED_INT8),     # Vehicle index of the vehicle triggering speed trap
        ("speed",                       DataTypes.FLOAT),             # Top speed achieved in kilometres per hour
        ("overallFastestInSession",   DataTypes.UNSIGNED_INT8),     # Overall fastest speed in session = 1, otherwise 0
        ("driverFastestInSession",    DataTypes.UNSIGNED_INT8),     # Fastest speed for driver in session = 1, otherwise 0
    ]

class StartLIghts(DataTypes.STRUCTURE):
    _fields_ = [
        ("numLights",   DataTypes.UNSIGNED_INT8)  # Number of lights showing
    ]

class DriveThroughPenaltyServed(DataTypes.STRUCTURE):
    _fields_ = [
        ("vehicleIdx",  DataTypes.UNSIGNED_INT8)  # Vehicle index of the vehicle serving drive through
    ]

class StopGoPenaltyServed(DataTypes.STRUCTURE):
    _fields_ = [
        ("vehicleIdx",  DataTypes.UNSIGNED_INT8)  # Vehicle index of the vehicle serving stop go
    ]

class Flashback(DataTypes.STRUCTURE):
    _fields_ = [
        ("flashbackFrameIdentifier",    DataTypes.UNSIGNED_INT32),    # Frame identifier flashed back to
        ("flashbackSessionTime",        DataTypes.FLOAT),             # Session time flashed back to
    ]

class Buttons(DataTypes.STRUCTURE):
    _fields_ = [
        ("m_buttonStatus",  DataTypes.UNSIGNED_INT32),    # Bit flags specifying which buttons are being pressed currently - see appendices
    ]

class EventDataDetails(DataTypes.UNION):
    _fields_ = [
        ("m_fastestLap",                FastestLap),
        ("m_retirement",                Retirement),
        ("m_teamMateInPits",            TeamMateInPits),
        ("m_raceWinner",                RaceWinner),
        ("m_penalty",                   Penalty),
        ("m_speedTrap",                 SpeedTrap),
        ("m_startLights",               StartLIghts),
        ("m_driveThroughPenaltyServed", DriveThroughPenaltyServed),
        ("m_stopGoPenaltyServed",       StopGoPenaltyServed),
        ("m_flashback",                 Flashback),
        ("m_buttons",                   Buttons),
    ]

class PacketEventData(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _enums_: dict[type, tuple[str, ...]] = {
        EVENT_STRING_CODE: ("m_eventStringCode",),
    }
    _fields_ = [
        ("m_header",            PacketHeader),                      # Header
        ("m_eventStringCode",   DataTypes.UNSIGNED_INT8 * 4), # Event string code
        ("m_eventDetails",      EventDataDetails),                  # Event details - should be interpreted differently for each type
    ]


### Participants Packet -- Every 5 seconds -- 1257 bytes

class ParticipantData(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _enums_: dict[type, tuple[str, ...]] = {
        DRIVER_ID: ("m_driverId",),
        TEAM_ID: ("m_teamId",),
        NATIONALITY_ID: ("m_nationality",),
    }
    _fields_ = [
        ("m_aiControlled",      DataTypes.UNSIGNED_INT8),     # Whether the vehicle is AI (1) or Human (0) controlled
        ("m_driverId",          DataTypes.UNSIGNED_INT8),     # Driver id - see appendix, 255 if network human
        ("m_networkId",         DataTypes.UNSIGNED_INT8),     # Network id – unique identifier for network players
        ("m_teamId",            DataTypes.UNSIGNED_INT8),     # Team id - see appendix
        ("m_myTeam",            DataTypes.UNSIGNED_INT8),     # My team flag – 1 = My Team, 0 = otherwise
        ("m_raceNumber",        DataTypes.UNSIGNED_INT8),     # Race number of the car
        ("m_nationality",       DataTypes.UNSIGNED_INT8),     # Nationality of the driver
        ("m_name",              DataTypes.CHAR * 48),         # Name of participant in UTF-8 format – null terminated, Will be truncated with … (U+2026) if too long
        ("m_yourTelemetry",     DataTypes.UNSIGNED_INT8),     # The player's UDP setting, 0 = restricted, 1 = public
    ]

class PacketParticipantsData(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_header",            PacketHeader),                      # Header
        ("m_numActiveCars",     DataTypes.UNSIGNED_INT8),     # Number of active cars in the data – should match number of cars on HUD
        ("m_participants",      ParticipantData * 22),
    ]


### Car Setups Packet -- 2 per second -- 1102 bytes

class CarSetupData(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_frontWing",                 DataTypes.UNSIGNED_INT8),     # Front wing aero
        ("m_rearWing",                  DataTypes.UNSIGNED_INT8),     # Rear wing aero
        ("m_onThrottle",                DataTypes.UNSIGNED_INT8),     # Differential adjustment on throttle (percentage)
        ("m_offThrottle",               DataTypes.UNSIGNED_INT8),     # Differential adjustment off throttle (percentage)
        ("m_frontCamber",               DataTypes.FLOAT),             # Front camber angle (suspension geometry)
        ("m_rearCamber",                DataTypes.FLOAT),             # Rear camber angle (suspension geometry)
        ("m_frontToe",                  DataTypes.FLOAT),             # Front toe angle (suspension geometry)
        ("m_rearToe",                   DataTypes.FLOAT),             # Rear toe angle (suspension geometry)
        ("m_frontSuspension",           DataTypes.UNSIGNED_INT8),     # Front suspension
        ("m_rearSuspension",            DataTypes.UNSIGNED_INT8),     # Rear suspension
        ("m_frontAntiRollBar",          DataTypes.UNSIGNED_INT8),     # Front anti-roll bar
        ("m_rearAntiRollBar",           DataTypes.UNSIGNED_INT8),     # Front anti-roll bar
        ("m_frontSuspensionHeight",     DataTypes.UNSIGNED_INT8),     # Front ride height
        ("m_rearSuspensionHeight",      DataTypes.UNSIGNED_INT8),     # Rear ride height
        ("m_brakePressure",             DataTypes.UNSIGNED_INT8),     # Brake pressure (percentage)
        ("m_brakeBias",                 DataTypes.UNSIGNED_INT8),     # Brake bias (percentage)
        ("m_rearLeftTyrePressure",      DataTypes.FLOAT),             # Rear left tyre pressure (PSI)
        ("m_rearRightTyrePressure",     DataTypes.FLOAT),             # Rear right tyre pressure (PSI)
        ("m_frontLeftTyrePressure",     DataTypes.FLOAT),             # Front left tyre pressure (PSI)
        ("m_frontRightTyrePressure",    DataTypes.FLOAT),             # Front right tyre pressure (PSI)
        ("m_ballast",                   DataTypes.UNSIGNED_INT8),     # Ballast
        ("m_fuelLoad",                  DataTypes.FLOAT),             # Fuel load
    ]

class PacketCarSetupData(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_header",                PacketHeader),              # Header
        ("m_car_setups",            CarSetupData * 22),
    ]


### Car Telemetry Packet -- Rate as specified in menus -- 1347 bytes

class CarTelemetryData(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _enums_: dict[type, tuple[str, ...]] = {
        SURFACE_TYPE: ("m_surfaceType",),
    }
    _fields_ = [
        ("m_speed",                     DataTypes.UNSIGNED_INT16),        # Speed of car in kilometres per hour
        ("m_throttle",                  DataTypes.FLOAT),                 # Amount of throttle applied (0.0 to 1.0)
        ("m_steer",                     DataTypes.FLOAT),                 # Steering (-1.0 (full lock left) to 1.0 (full lock right))
        ("m_brake",                     DataTypes.FLOAT),                 # Amount of brake applied (0.0 to 1.0)
        ("m_clutch",                    DataTypes.UNSIGNED_INT8),         # Amount of clutch applied (0 to 100)
        ("m_gear",                      DataTypes.SIGNED_INT8),           # Gear selected (1-8, N=0, R=-1)
        ("m_engineRpm",                 DataTypes.UNSIGNED_INT16),        # Engine RPM
        ("m_drs",                       DataTypes.UNSIGNED_INT8),         # 0 = off, 1 = on
        ("m_revLightsPercent",          DataTypes.UNSIGNED_INT8),         # Rev lights indicator (percentage)
        ("m_revLightsBitValue",         DataTypes.UNSIGNED_INT16),        # Rev lights (bit 0 = leftmost LED, bit 14 = rightmost LED)
        ("m_brakesTemperature",         DataTypes.UNSIGNED_INT16 * 4),    # Brakes temperature (celsius)
        ("m_tyresSurfaceTemperature",   DataTypes.UNSIGNED_INT8 * 4),     # Tyres surface temperature (celsius)
        ("m_tyresInnerTemperature",     DataTypes.UNSIGNED_INT8 * 4),     # Tyres inner temperature (celsius)
        ("m_engineTemperature",         DataTypes.UNSIGNED_INT16),        # Engine temperature (celsius)
        ("m_tyresPressure",             DataTypes.FLOAT * 4),             # Tyres pressure (PSI)
        ("m_surfaceType",               DataTypes.UNSIGNED_INT8 * 4),     # Driving surface, see appendices
    ]

class PacketCarTelemetryData(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_header",                        PacketHeader),                      # Header
        ("m_carTelemetryData",              CarTelemetryData * 22),
        ("m_mfdPanelIndex",                 DataTypes.UNSIGNED_INT8),     # Index of MFD panel open - 255 = MFD closed, Single player, race – 0 = Car setup, 1 = Pits, 2 = Damage, 3 =  Engine, 4 = Temperatures - May vary depending on game mode
        ("m_mfdPanelIndexSecondaryPlayer",  DataTypes.UNSIGNED_INT8),     # See above
        ("m_suggestedGear",                 DataTypes.SIGNED_INT8),       # Suggested gear for the player (1-8), 0 if no gear suggested
    ]


### Car Status Packet -- Rate as specified in menus -- 1058 bytes

class CarStatusData(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_tractionControl",           DataTypes.UNSIGNED_INT8),     # Traction control - 0 = off, 1 = medium, 2 = full
        ("m_antiLockBrakes",            DataTypes.UNSIGNED_INT8),     # 0 (off) - 1 (on)
        ("m_fuelMix",                   DataTypes.UNSIGNED_INT8),     # Fuel mix - 0 = lean, 1 = standard, 2 = rich, 3 = max
        ("m_frontBrakeBias",            DataTypes.UNSIGNED_INT8),     # Front brake bias (percentage)
        ("m_pitLimiterStatus",          DataTypes.UNSIGNED_INT8),     # Pit limiter status - 0 = off, 1 = on
        ("m_fuelInTank",                DataTypes.FLOAT),             # Current fuel mass
        ("m_fuelCapacity",              DataTypes.FLOAT),             # Fuel capacity
        ("m_fuelRemainingLaps",         DataTypes.FLOAT),             # Fuel remaining in terms of laps (value on MFD)
        ("m_maxRpm",                    DataTypes.UNSIGNED_INT16),    # Cars max RPM, point of rev limiter
        ("m_idleRpm",                   DataTypes.UNSIGNED_INT16),    # Cars idle RPM
        ("m_maxGears",                  DataTypes.UNSIGNED_INT8),     # Maximum number of gears
        ("m_drsAllowed",                DataTypes.UNSIGNED_INT8),     # 0 = not allowed, 1 = allowed
        ("m_drsActivationDistance",     DataTypes.UNSIGNED_INT16),    # 0 = DRS not available, non-zero - DRS will be available in [X] metres
        ("m_actualTyreCompound",        DataTypes.UNSIGNED_INT8),     # F1 Modern - 16 = C5, 17 = C4, 18 = C3, 19 = C2, 20 = C1, 21 = C0, 7 = inter, 8 = wet
                                                                            # F1 Classic - 9 = dry, 10 = wet
                                                                            # F2 – 11 = super soft, 12 = soft, 13 = medium, 14 = hard, 15 = wet
        ("m_visualTyreCompound",        DataTypes.UNSIGNED_INT8),     # F1 visual (can be different from actual compound) - 16 = soft, 17 = medium, 18 = hard, 7 = inter, 8 = wet
                                                                            # F1 Classic – same as above
                                                                            # F2 ‘19, 15 = wet, 19 – super soft, 20 = soft, 21 = medium , 22 = hard
        ("m_tyresAgeLaps",              DataTypes.UNSIGNED_INT8),     # Age in laps of the current set of tyres
        ("m_vehicleFiaFlags",           DataTypes.SIGNED_INT8),       # -1 = invalid/unknown, 0 = none, 1 = green, 2 = blue, 3 = yellow
        ("m_ersStoreEnergy",            DataTypes.FLOAT),             # ERS energy store in Joules
        ("m_ersDeployMode",             DataTypes.UNSIGNED_INT8),     # ERS deployment mode, 0 = none, 1 = medium, 2 = hotlap, 3 = overtake
        ("m_ersHarvestedThisLapMguk",   DataTypes.FLOAT),             # ERS energy harvested this lap by MGU-K
        ("m_ersHarvestedThisLapMguh",   DataTypes.FLOAT),             # ERS energy harvested this lap by MGU-H
        ("m_ersDeployedThisLap",        DataTypes.FLOAT),             # ERS energy deployed this lap
        ("m_networkPaused",             DataTypes.UNSIGNED_INT8),     # Whether the car is paused in a network game
    ]

class PacketCarStatusData(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_header",        PacketHeader),          # Header
        ("m_carStatusData", CarStatusData * 22),
    ]


### Final Classification Packet -- Once at the end of a race -- 839 bytes

class FinalClassificationData(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_position",          DataTypes.UNSIGNED_INT8),         # Finishing position
        ("m_numLaps",           DataTypes.UNSIGNED_INT8),         # Number of laps completed
        ("m_gridPosition",      DataTypes.UNSIGNED_INT8),         # Grid position of the car
        ("m_points",            DataTypes.UNSIGNED_INT8),         # Number of points scored
        ("m_numPitStops",       DataTypes.UNSIGNED_INT8),         # Number of pit stops made
        ("m_resultStatus",      DataTypes.UNSIGNED_INT8),         # Result status - 0 = invalid, 1 = inactive, 2 = active, 3 = finished, 4 = didnotfinish, 5 = disqualified, 6 = not classified, 7 = retired
        ("m_bestLapTimeInMs",   DataTypes.UNSIGNED_INT32),        # Best lap time of the session in milliseconds
        ("m_totalRaceTime",     DataTypes.DOUBLE),                # Total race time in seconds without penalties
        ("m_penaltiesTime",     DataTypes.UNSIGNED_INT8),         # Total penalties accumulated in seconds
        ("m_numPenalties",      DataTypes.UNSIGNED_INT8),         # Number of penalties applied to this driver
        ("m_numTyreStints",     DataTypes.UNSIGNED_INT8),         # Number of tyres stints up to maximum
        ("m_tyreStintsActual",  DataTypes.UNSIGNED_INT8 * 8),     # Actual tyres used by this driver
        ("m_tyreStintsVisual",  DataTypes.UNSIGNED_INT8 * 8),     # Visual tyres used by this driver
    ]

class PacketFinalClassificationData(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_header",                PacketHeader),                      # Header
        ("m_numCars",               DataTypes.UNSIGNED_INT8),     # Number of cars in the final classification
        ("m_classificationData",    FinalClassificationData * 22),
    ]


### Lobby Info Packet -- Two every second when in the lobby -- 1191 bytes

class LobbyInfoData(DataTypes.STRUCTURE):
    _enums_: dict[type, tuple[str, ...]] = {
        TEAM_ID: ("m_teamId",),
        NATIONALITY_ID: ("m_nationality",),
    }
    _fields_ = [
        ("m_aiControlled",      DataTypes.UNSIGNED_INT8),     # Whether the vehicle is AI (1) or Human (0) controlled
        ("m_teamId",            DataTypes.UNSIGNED_INT8),     # Team id - see appendix (255 if no team currently selected)
        ("m_nationality",       DataTypes.UNSIGNED_INT8),     # Nationality of the driver
        ("m_name",              DataTypes.CHAR * 48),         # Name of participant in UTF-8 format – null terminated Will be truncated with ... (U+2026) if too long
        ("m_carNumber",         DataTypes.UNSIGNED_INT8),     # Car number of the player
        ("m_readyStatus",       DataTypes.UNSIGNED_INT8),     # 0 = not ready, 1 = ready, 2 = spectating
    ]

class PacketLobbyInfoData(DataTypes.STRUCTURE):
    _fields_ = [
        ("m_header",        PacketHeader),                      # Header Packet specific data
        ("m_numPlayers",    DataTypes.UNSIGNED_INT8),     # Number of players in the lobby data
        ("m_lobbyPlayers",  LobbyInfoData * 22),
    ]


### Car Damage Packet -- 10 per second -- 882 bytes

class CarDamageData(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_tyresWear",             DataTypes.FLOAT * 4),             # Tyre wear (percentage)
        ("m_tyresDamage",           DataTypes.UNSIGNED_INT8 * 4),     # Tyre damage (percentage)
        ("m_brakesDamage",          DataTypes.UNSIGNED_INT8 * 4),     # Brakes damage (percentage)
        ("m_frontLeftWingDamage",   DataTypes.UNSIGNED_INT8),         # Front left wing damage (percentage)
        ("m_frontRightWingDamage",  DataTypes.UNSIGNED_INT8),         # Front right wing damage (percentage)
        ("m_rearWingDamage",        DataTypes.UNSIGNED_INT8),         # Rear wing damage (percentage)
        ("m_floorDamage",           DataTypes.UNSIGNED_INT8),         # Floor damage (percentage)
        ("m_diffuserDamage",        DataTypes.UNSIGNED_INT8),         # Diffuser damage (percentage)
        ("m_sidepodDamage",         DataTypes.UNSIGNED_INT8),         # Sidepod damage (percentage)
        ("m_drsFault",              DataTypes.UNSIGNED_INT8),         # Indicator for DRS fault, 0 = OK, 1 = fault
        ("m_gearBoxDamage",         DataTypes.UNSIGNED_INT8),         # Gear box damage (percentage)
        ("m_engineDamage",          DataTypes.UNSIGNED_INT8),         # Engine damage (percentage)
        ("m_engineMGUHWear",        DataTypes.UNSIGNED_INT8),         # Engine wear MGU-H (percentage)
        ("m_engineESWear",          DataTypes.UNSIGNED_INT8),         # Engine wear ES (percentage)
        ("m_engineCEWear",          DataTypes.UNSIGNED_INT8),         # Engine wear CE (percentage)
        ("m_engineICEWear",         DataTypes.UNSIGNED_INT8),         # Engine wear ICE (percentage)
        ("m_engineMGUKWear",        DataTypes.UNSIGNED_INT8),         # Engine wear MGU-K (percentage)
        ("m_engineTCWear",          DataTypes.UNSIGNED_INT8),         # Engine wear TC (percentage)
    ]

class PacketCarDamageData(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_header",            PacketHeader),          # Header
        ("m_carDamageData",     CarDamageData * 22),
    ]


### Session History Packet -- 20 per second but cycling through cars -- 1155 bytes

class LapHistoryData(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_lapTimeInMs",           DataTypes.UNSIGNED_INT32),    # Lap time in milliseconds
        ("m_sector1TimeInMs",       DataTypes.UNSIGNED_INT16),    # Sector 1 time in milliseconds
        ("m_sector2TimeInMs",       DataTypes.UNSIGNED_INT16),    # Sector 2 time in millisecond
        ("m_sector3TimeInMs",       DataTypes.UNSIGNED_INT16),    # Sector 3 time in milliseconds
        ("m_lapValidBitFlags",      DataTypes.UNSIGNED_INT8),     # 0x01 bit set-lap valid, 0x02 bit set-sector 1 valid, 0x04 bit set-sector 2 valid, 0x08 bit set-sector 3 valid
    ]

class TyreStintHistoryData(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_endLap",                DataTypes.UNSIGNED_INT8),     # Lap the tyre usage ends on (255 of current tyre)
        ("m_tyreActualCompound",    DataTypes.UNSIGNED_INT8),     # Actual tyres used by this driver
        ("m_tyreVisualCompound",    DataTypes.UNSIGNED_INT8),     # Visual tyres used by this driver
    ]

class PacketSessionHistoryData(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_header",                    PacketHeader),                      # Header
        ("m_carIdx",                    DataTypes.UNSIGNED_INT8),     # Index of the car this lap data relates to
        ("m_numLaps",                   DataTypes.UNSIGNED_INT8),     # Num laps in the data (including current partial lap)
        ("m_numTyreStints",             DataTypes.UNSIGNED_INT8),     # Number of tyre stints in the data
        ("m_bestLapTimeLapNum",         DataTypes.UNSIGNED_INT8),     # Lap the best lap time was achieved on
        ("m_bestSector1LapNum",         DataTypes.UNSIGNED_INT8),     # Lap the best Sector 1 time was achieved on
        ("m_bestSector2LapNum",         DataTypes.UNSIGNED_INT8),     # Lap the best Sector 2 time was achieved on
        ("m_bestSector3LapNum",         DataTypes.UNSIGNED_INT8),     # Lap the best Sector 3 time was achieved on
        ("m_lapHistoryData",            LapHistoryData * 100),              # 100 laps of data max
        ("m_tyreStintsHistoryData",     TyreStintHistoryData * 8),
    ]


### * MetaData

class MetaData:
    # standard network info
    port: int | None = 20777
    
    # use if a heartbeat is needed
    heartBeatPort: int | None = None
    heartBeatFunc = None
    
    # use for itinial hand shake
    handShakePort: int | None = None
    handShakeFunc: tuple | None = None
    
    # use if the data needs decrypting
    decrytionFunc = None
    
    # use if there is a header packet
    headerInfo: type | None = PacketHeader
    packetIDAttribute: str | None = "m_packetId"
    
    # use for shared memory
    allSharedMemoryNames: str | None | dict[str, str] = None
    
    # standard packet info
    packetInfo: dict[int, tuple[type, ...]] = {
        0: (PacketMotionData,),                 # Contains all motion data for player’s car – only sent while player is in control
        1: (PacketSessionData,),                # Data about the session – track, time left
        2: (PacketLapData,),                    # Data about all the lap times of cars in the session
        3: (PacketEventData,),                  # Various notable events that happen during a session
        4: (PacketParticipantsData,),           # List of participants in the session, mostly relevant for multiplayer
        5: (PacketCarSetupData,),               # Packet detailing car setups for cars in the race
        6: (PacketCarTelemetryData,),           # Telemetry data for all cars
        7: (PacketCarStatusData,),              # Status data for all cars
        8: (PacketFinalClassificationData,),    # Final classification confirmation at the end of a race
        9: (PacketLobbyInfoData,),              # Information about players in a multiplayer lobby
        10: (PacketCarDamageData,),             # Damage status for all cars
        11: (PacketSessionHistoryData,),        # Lap and tyre data for session
    }

