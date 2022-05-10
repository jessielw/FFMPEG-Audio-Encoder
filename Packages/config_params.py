from configparser import ConfigParser
from tkinter import messagebox


def create_config_params():
    # Bundled apps config ---------------------------------------------------------------------------------------------

    config_file = 'Runtime/config.ini'  # Creates (if doesn't exist) and defines location of config.ini
    config = ConfigParser()
    config.read(config_file)

    if not config.has_section('output_path'):  # Create config parameters
        config.add_section('output_path')
    if not config.has_option('output_path', 'path'):
        config.set('output_path', 'path', 'file input directory')
    if not config.has_section('ffmpeg_path'):  # Create config parameters
        config.add_section('ffmpeg_path')
    if not config.has_option('ffmpeg_path', 'path'):
        config.set('ffmpeg_path', 'path', '')
    if not config.has_section('mpv_player_path'):
        config.add_section('mpv_player_path')
    if not config.has_option('mpv_player_path', 'path'):
        config.set('mpv_player_path', 'path', '')
    if not config.has_section('mediainfogui_path'):
        config.add_section('mediainfogui_path')
    if not config.has_option('mediainfogui_path', 'path'):
        config.set('mediainfogui_path', 'path', '')
    if not config.has_section('mediainfocli_path'):
        config.add_section('mediainfocli_path')
    if not config.has_option('mediainfocli_path', 'path'):
        config.set('mediainfocli_path', 'path', '')
    if not config.has_section('debug_option'):
        config.add_section('debug_option')
    if not config.has_option('debug_option', 'option'):
        config.set('debug_option', 'option', '')
    if not config.has_section('auto_close_progress_window'):
        config.add_section('auto_close_progress_window')
    if not config.has_option('auto_close_progress_window', 'option'):
        config.set('auto_close_progress_window', 'option', '')
    if not config.has_section('audio_settings_command_toggle'):
        config.add_section('audio_settings_command_toggle')
    if not config.has_option('audio_settings_command_toggle', 'option'):
        config.set('audio_settings_command_toggle', 'option', '')
    if not config.has_section('save_window_locations'):
        config.add_section('save_window_locations')
    if not config.has_option('save_window_locations', 'ffmpeg audio encoder'):
        config.set('save_window_locations', 'ffmpeg audio encoder', 'yes')
    if not config.has_option('save_window_locations', 'ffmpeg audio encoder position'):
        config.set('save_window_locations', 'ffmpeg audio encoder position', '')
    if not config.has_option('save_window_locations', 'window location settings'):
        config.set('save_window_locations', 'window location settings', 'yes')
    if not config.has_option('save_window_locations', 'window location settings position'):
        config.set('save_window_locations', 'window location settings position', '')
    if not config.has_option('save_window_locations', 'about'):
        config.set('save_window_locations', 'about', 'yes')
    if not config.has_option('save_window_locations', 'about position'):
        config.set('save_window_locations', 'about position', '')
    if not config.has_option('save_window_locations', 'progress window'):
        config.set('save_window_locations', 'progress window', 'yes')
    if not config.has_option('save_window_locations', 'progress window position'):
        config.set('save_window_locations', 'progress window position', '')
    if not config.has_option('save_window_locations', 'job window'):
        config.set('save_window_locations', 'job window', 'yes')
    if not config.has_option('save_window_locations', 'job window position'):
        config.set('save_window_locations', 'job window position', '')
    if not config.has_option('save_window_locations', 'display command'):
        config.set('save_window_locations', 'display command', 'yes')
    if not config.has_option('save_window_locations', 'display command position'):
        config.set('save_window_locations', 'display command position', '')
    if not config.has_option('save_window_locations', 'general settings'):
        config.set('save_window_locations', 'general settings', 'yes')
    if not config.has_option('save_window_locations', 'general settings position'):
        config.set('save_window_locations', 'general settings position', '')
    if not config.has_option('save_window_locations', 'audio window - aac'):
        config.set('save_window_locations', 'audio window - aac', 'yes')
    if not config.has_option('save_window_locations', 'audio window - aac - position'):
        config.set('save_window_locations', 'audio window - aac - position', '')
    if not config.has_option('save_window_locations', 'audio window - ac3'):
        config.set('save_window_locations', 'audio window - ac3', 'yes')
    if not config.has_option('save_window_locations', 'audio window - ac3 - position'):
        config.set('save_window_locations', 'audio window - ac3 - position', '')
    if not config.has_option('save_window_locations', 'audio window - e-ac3'):
        config.set('save_window_locations', 'audio window - e-ac3', 'yes')
    if not config.has_option('save_window_locations', 'audio window - e-ac3 - position'):
        config.set('save_window_locations', 'audio window - e-ac3 - position', '')
    if not config.has_option('save_window_locations', 'audio window - dts'):
        config.set('save_window_locations', 'audio window - dts', 'yes')
    if not config.has_option('save_window_locations', 'audio window - dts - position'):
        config.set('save_window_locations', 'audio window - dts - position', '')
    if not config.has_option('save_window_locations', 'audio window - opus'):
        config.set('save_window_locations', 'audio window - opus', 'yes')
    if not config.has_option('save_window_locations', 'audio window - opus - position'):
        config.set('save_window_locations', 'audio window - opus - position', '')
    if not config.has_option('save_window_locations', 'audio window - mp3'):
        config.set('save_window_locations', 'audio window - mp3', 'yes')
    if not config.has_option('save_window_locations', 'audio window - mp3 - position'):
        config.set('save_window_locations', 'audio window - mp3 - position', '')
    if not config.has_option('save_window_locations', 'audio window - fdk-aac'):
        config.set('save_window_locations', 'audio window - fdk-aac', 'yes')
    if not config.has_option('save_window_locations', 'audio window - fdk-aac - position'):
        config.set('save_window_locations', 'audio window - fdk-aac - position', '')
    if not config.has_option('save_window_locations', 'audio window - qaac'):
        config.set('save_window_locations', 'audio window - qaac', 'yes')
    if not config.has_option('save_window_locations', 'audio window - qaac - position'):
        config.set('save_window_locations', 'audio window - qaac - position', '')
    if not config.has_option('save_window_locations', 'audio window - flac'):
        config.set('save_window_locations', 'audio window - flac', 'yes')
    if not config.has_option('save_window_locations', 'audio window - flac - position'):
        config.set('save_window_locations', 'audio window - flac - position', '')
    if not config.has_option('save_window_locations', 'audio window - alac'):
        config.set('save_window_locations', 'audio window - alac', 'yes')
    if not config.has_option('save_window_locations', 'audio window - alac - position'):
        config.set('save_window_locations', 'audio window - alac - position', '')
    if not config.has_option('save_window_locations', 'audio window - view streams'):
        config.set('save_window_locations', 'audio window - view streams', 'yes')
    if not config.has_option('save_window_locations', 'audio window - view streams - position'):
        config.set('save_window_locations', 'audio window - view streams - position', '')

    try:
        with open(config_file, 'w') as configfile:
            config.write(configfile)
    except (Exception,):
        messagebox.showinfo(title='Error', message='Could Not Write to config.ini file, delete and try again')
    # Bundled apps config ---------------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------------------- Profile Config
    config_profile_ini = 'Runtime/profiles.ini'  # Creates (if doesn't exist) and defines location of profile.ini
    config_profile = ConfigParser()
    config_profile.read(config_profile_ini)

    # AAC settings --------------------------------------------------- # Create config parameters
    if not config_profile.has_section('FFMPEG AAC - SETTINGS'):
        config_profile.add_section('FFMPEG AAC - SETTINGS')
    if not config_profile.has_option('FFMPEG AAC - SETTINGS', 'dolbyprologicii'):
        config_profile.set('FFMPEG AAC - SETTINGS', 'dolbyprologicii', '')
    if not config_profile.has_option('FFMPEG AAC - SETTINGS', 'ffmpeg_volume'):
        config_profile.set('FFMPEG AAC - SETTINGS', 'ffmpeg_volume', '0.0')
    if not config_profile.has_option('FFMPEG AAC - SETTINGS', 'aac_bitrate'):
        config_profile.set('FFMPEG AAC - SETTINGS', 'aac_bitrate', '192')
    if not config_profile.has_option('FFMPEG AAC - SETTINGS', 'aac_vbr_quality'):
        config_profile.set('FFMPEG AAC - SETTINGS', 'aac_vbr_quality', '2')
    if not config_profile.has_option('FFMPEG AAC - SETTINGS', 'aac_vbr_toggle'):
        config_profile.set('FFMPEG AAC - SETTINGS', 'aac_vbr_toggle', '-c:a')
    if not config_profile.has_option('FFMPEG AAC - SETTINGS', 'aac_channel'):
        config_profile.set('FFMPEG AAC - SETTINGS', 'aac_channel', 'Original')
    if not config_profile.has_option('FFMPEG AAC - SETTINGS', 'samplerate'):
        config_profile.set('FFMPEG AAC - SETTINGS', 'samplerate', 'Original')
    if not config_profile.has_option('FFMPEG AAC - SETTINGS', 'tempo'):
        config_profile.set('FFMPEG AAC - SETTINGS', 'tempo', 'Original')
    # --------------------------------------------------- AAC Settings
    # AC3 settings --------------------------------------------------- # Create config parameters
    if not config_profile.has_section('FFMPEG AC3 - SETTINGS'):
        config_profile.add_section('FFMPEG AC3 - SETTINGS')
    if not config_profile.has_option('FFMPEG AC3 - SETTINGS', 'ac3_bitrate'):
        config_profile.set('FFMPEG AC3 - SETTINGS', 'ac3_bitrate', '224k')
    if not config_profile.has_option('FFMPEG AC3 - SETTINGS', 'dolbyprologicii'):
        config_profile.set('FFMPEG AC3 - SETTINGS', 'dolbyprologicii', '')
    if not config_profile.has_option('FFMPEG AC3 - SETTINGS', 'ffmpeg_volume'):
        config_profile.set('FFMPEG AC3 - SETTINGS', 'ffmpeg_volume', '0.0')
    if not config_profile.has_option('FFMPEG AC3 - SETTINGS', 'ac3_channel'):
        config_profile.set('FFMPEG AC3 - SETTINGS', 'ac3_channel', 'Original')
    if not config_profile.has_option('FFMPEG AC3 - SETTINGS', 'samplerate'):
        config_profile.set('FFMPEG AC3 - SETTINGS', 'samplerate', 'Original')
    if not config_profile.has_option('FFMPEG AC3 - SETTINGS', 'tempo'):
        config_profile.set('FFMPEG AC3 - SETTINGS', 'tempo', 'Original')
    # --------------------------------------------------- AC3 Settings
    # DTS settings --------------------------------------------------- # Create config parameters
    if not config_profile.has_section('FFMPEG DTS - SETTINGS'):
        config_profile.add_section('FFMPEG DTS - SETTINGS')
    if not config_profile.has_option('FFMPEG DTS - SETTINGS', 'dts_bitrate'):
        config_profile.set('FFMPEG DTS - SETTINGS', 'dts_bitrate', '448')
    if not config_profile.has_option('FFMPEG DTS - SETTINGS', 'dolbyprologicii'):
        config_profile.set('FFMPEG DTS - SETTINGS', 'dolbyprologicii', '')
    if not config_profile.has_option('FFMPEG DTS - SETTINGS', 'ffmpeg_volume'):
        config_profile.set('FFMPEG DTS - SETTINGS', 'ffmpeg_volume', '0.0')
    if not config_profile.has_option('FFMPEG DTS - SETTINGS', 'dts_channel'):
        config_profile.set('FFMPEG DTS - SETTINGS', 'dts_channel', '2 (Stereo)')
    if not config_profile.has_option('FFMPEG DTS - SETTINGS', 'samplerate'):
        config_profile.set('FFMPEG DTS - SETTINGS', 'samplerate', 'Original')
    if not config_profile.has_option('FFMPEG DTS - SETTINGS', 'tempo'):
        config_profile.set('FFMPEG DTS - SETTINGS', 'tempo', 'Original')
    # --------------------------------------------------- DTS Settings
    # E-AC3 settings --------------------------------------------------- # Create config parameters
    if not config_profile.has_section('FFMPEG E-AC3 - SETTINGS'):
        config_profile.add_section('FFMPEG E-AC3 - SETTINGS')
    if not config_profile.has_option('FFMPEG E-AC3 - SETTINGS', 'e-ac3_bitrate'):
        config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_bitrate', '448k')
    if not config_profile.has_option('FFMPEG E-AC3 - SETTINGS', 'e-ac3_channel'):
        config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_channel', 'Original')
    if not config_profile.has_option('FFMPEG E-AC3 - SETTINGS', 'e-ac3_volume'):
        config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_volume', '0.0')
    if not config_profile.has_option('FFMPEG E-AC3 - SETTINGS', 'samplerate'):
        config_profile.set('FFMPEG E-AC3 - SETTINGS', 'samplerate', 'Original')
    if not config_profile.has_option('FFMPEG E-AC3 - SETTINGS', 'e-ac3_per_frame_metadata'):
        config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_per_frame_metadata', 'Default')
    if not config_profile.has_option('FFMPEG E-AC3 - SETTINGS', 'e-ac3_mixing_level'):
        config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_mixing_level', '-1')
    if not config_profile.has_option('FFMPEG E-AC3 - SETTINGS', 'e-ac3_room_type'):
        config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_room_type', 'Default')
    if not config_profile.has_option('FFMPEG E-AC3 - SETTINGS', 'e-ac3_copyright_bit'):
        config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_copyright_bit', '-1')
    if not config_profile.has_option('FFMPEG E-AC3 - SETTINGS', 'e-ac3_dialogue_level'):
        config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_dialogue_level', '-31')
    if not config_profile.has_option('FFMPEG E-AC3 - SETTINGS', 'e-ac3_surround_mode'):
        config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_surround_mode', 'Default')
    if not config_profile.has_option('FFMPEG E-AC3 - SETTINGS', 'e-ac3_original_bitstream'):
        config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_original_bitstream', '-1')
    if not config_profile.has_option('FFMPEG E-AC3 - SETTINGS', 'e-ac3_downmix_mode'):
        config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_downmix_mode', 'Default')
    if not config_profile.has_option('FFMPEG E-AC3 - SETTINGS', 'e-ac3_lt_rt_center_mix'):
        config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_lt_rt_center_mix', '-1')
    if not config_profile.has_option('FFMPEG E-AC3 - SETTINGS', 'e-ac3_lt_rt_surround_mix'):
        config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_lt_rt_surround_mix', '-1')
    if not config_profile.has_option('FFMPEG E-AC3 - SETTINGS', 'e-ac3_lo_ro_center_mix'):
        config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_lo_ro_center_mix', '-1')
    if not config_profile.has_option('FFMPEG E-AC3 - SETTINGS', 'e-ac3_lo_ro_surround_mix'):
        config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_lo_ro_surround_mix', '-1')
    if not config_profile.has_option('FFMPEG E-AC3 - SETTINGS', 'e-ac3_dolby_surround_ex_mode'):
        config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_dolby_surround_ex_mode', 'Default')
    if not config_profile.has_option('FFMPEG E-AC3 - SETTINGS', 'e-ac3_dolby_headphone_mode'):
        config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_dolby_headphone_mode', 'Default')
    if not config_profile.has_option('FFMPEG E-AC3 - SETTINGS', 'e-ac3_a_d_converter_type'):
        config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_a_d_converter_type', 'Default')
    if not config_profile.has_option('FFMPEG E-AC3 - SETTINGS', 'e-ac3_stereo_rematrixing'):
        config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_dolby_stereo_rematrixing', 'Default')
    if not config_profile.has_option('FFMPEG E-AC3 - SETTINGS', 'e-ac3_channel_coupling'):
        config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_channel_coupling', '-1')
    if not config_profile.has_option('FFMPEG E-AC3 - SETTINGS', 'e-ac3_cpl_start_band'):
        config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_cpl_start_band', '-1')
    if not config_profile.has_option('FFMPEG E-AC3 - SETTINGS', 'tempo'):
        config_profile.set('FFMPEG E-AC3 - SETTINGS', 'tempo', 'Original')
    # --------------------------------------------------- E-AC3 Settings
    # Opus settings --------------------------------------------------- # Create config parameters
    if not config_profile.has_section('FFMPEG Opus - SETTINGS'):
        config_profile.add_section('FFMPEG Opus - SETTINGS')
    if not config_profile.has_option('FFMPEG Opus - SETTINGS', 'opus_bitrate'):
        config_profile.set('FFMPEG Opus - SETTINGS', 'opus_bitrate', '160k')
    if not config_profile.has_option('FFMPEG Opus - SETTINGS', 'samplerate'):
        config_profile.set('FFMPEG Opus - SETTINGS', 'samplerate', 'Original')
    if not config_profile.has_option('FFMPEG Opus - SETTINGS', 'acodec_vbr'):
        config_profile.set('FFMPEG Opus - SETTINGS', 'acodec_vbr', 'VBR: On')
    if not config_profile.has_option('FFMPEG Opus - SETTINGS', 'acodec_application'):
        config_profile.set('FFMPEG Opus - SETTINGS', 'acodec_application', 'Audio')
    if not config_profile.has_option('FFMPEG Opus - SETTINGS', 'frame_duration'):
        config_profile.set('FFMPEG Opus - SETTINGS', 'frame_duration', '20')
    if not config_profile.has_option('FFMPEG Opus - SETTINGS', 'packet_loss'):
        config_profile.set('FFMPEG Opus - SETTINGS', 'packet_loss', '0')
    if not config_profile.has_option('FFMPEG Opus - SETTINGS', 'acodec_channel'):
        config_profile.set('FFMPEG Opus - SETTINGS', 'acodec_channel', '2 (Stereo)')
    if not config_profile.has_option('FFMPEG Opus - SETTINGS', 'dolbyprologicii'):
        config_profile.set('FFMPEG Opus - SETTINGS', 'dolbyprologicii', '')
    if not config_profile.has_option('FFMPEG Opus - SETTINGS', 'ffmpeg_volume'):
        config_profile.set('FFMPEG Opus - SETTINGS', 'ffmpeg_volume', '0.0')
    if not config_profile.has_option('FFMPEG Opus - SETTINGS', 'tempo'):
        config_profile.set('FFMPEG Opus - SETTINGS', 'tempo', 'Original')
    if not config_profile.has_option('FFMPEG Opus - SETTINGS', 'mapping_family'):
        config_profile.set('FFMPEG Opus - SETTINGS', 'mapping_family', 'Mapping -1: Auto')
    # --------------------------------------------------- Opus Settings
    # FDK-AAC settings --------------------------------------------------- # Create config parameters
    if not config_profile.has_section('FDK-AAC - SETTINGS'):
        config_profile.add_section('FDK-AAC - SETTINGS')
    if not config_profile.has_option('FDK-AAC - SETTINGS', 'fdk_aac_bitrate'):
        config_profile.set('FDK-AAC - SETTINGS', 'fdk_aac_bitrate', 'CBR: 192k')
    if not config_profile.has_option('FDK-AAC - SETTINGS', 'acodec_channel'):
        config_profile.set('FDK-AAC - SETTINGS', 'acodec_channel', 'Original')
    if not config_profile.has_option('FDK-AAC - SETTINGS', 'dolbyprologicii'):
        config_profile.set('FDK-AAC - SETTINGS', 'dolbyprologicii', '')
    if not config_profile.has_option('FDK-AAC - SETTINGS', 'ffmpeg_volume'):
        config_profile.set('FDK-AAC - SETTINGS', 'ffmpeg_volume', '0.0')
    if not config_profile.has_option('FDK-AAC - SETTINGS', 'samplerate'):
        config_profile.set('FDK-AAC - SETTINGS', 'samplerate', 'Original')
    if not config_profile.has_option('FDK-AAC - SETTINGS', 'fdk_aac_profile'):
        config_profile.set('FDK-AAC - SETTINGS', 'fdk_aac_profile', 'AAC LC (Default)')
    if not config_profile.has_option('FDK-AAC - SETTINGS', 'fdk_aac_lowdelay'):
        config_profile.set('FDK-AAC - SETTINGS', 'fdk_aac_lowdelay', 'Disable SBR on ELD (DEF)')
    if not config_profile.has_option('FDK-AAC - SETTINGS', 'fdk_aac_sbr_ratio'):
        config_profile.set('FDK-AAC - SETTINGS', 'fdk_aac_sbr_ratio', 'Library Default')
    if not config_profile.has_option('FDK-AAC - SETTINGS', 'fdk_aac_gapless'):
        config_profile.set('FDK-AAC - SETTINGS', 'fdk_aac_gapless', 'iTunSMPB (Def)')
    if not config_profile.has_option('FDK-AAC - SETTINGS', 'fdk_aac_transport_format'):
        config_profile.set('FDK-AAC - SETTINGS', 'fdk_aac_transport_format', 'M4A (Def)')
    if not config_profile.has_option('FDK-AAC - SETTINGS', 'fdk_aac_afterburner'):
        config_profile.set('FDK-AAC - SETTINGS', 'fdk_aac_afterburner', '-a1')
    if not config_profile.has_option('FDK-AAC - SETTINGS', 'fdk_aac_crccheck'):
        config_profile.set('FDK-AAC - SETTINGS', 'fdk_aac_crccheck', '')
    if not config_profile.has_option('FDK-AAC - SETTINGS', 'fdk_aac_headerperiod'):
        config_profile.set('FDK-AAC - SETTINGS', 'fdk_aac_headerperiod', '')
    if not config_profile.has_option('FDK-AAC - SETTINGS', 'fdk_aac_sbrdelay'):
        config_profile.set('FDK-AAC - SETTINGS', 'fdk_aac_sbrdelay', '')
    if not config_profile.has_option('FDK-AAC - SETTINGS', 'fdk_aac_moovbox'):
        config_profile.set('FDK-AAC - SETTINGS', 'fdk_aac_moovbox', '')
    if not config_profile.has_option('FDK-AAC - SETTINGS', 'fdk_aac_tempo'):
        config_profile.set('FDK-AAC - SETTINGS', 'fdk_aac_tempo', 'Original')
    # --------------------------------------------------- FDK-AAC Settings
    # MP3 settings --------------------------------------------------- # Create config parameters
    if not config_profile.has_section('FFMPEG MP3 - SETTINGS'):
        config_profile.add_section('FFMPEG MP3 - SETTINGS')
    if not config_profile.has_option('FFMPEG MP3 - SETTINGS', 'acodec_bitrate'):
        config_profile.set('FFMPEG MP3 - SETTINGS', 'acodec_bitrate', 'VBR: -V 0')
    if not config_profile.has_option('FFMPEG MP3 - SETTINGS', 'acodec_channel'):
        config_profile.set('FFMPEG MP3 - SETTINGS', 'acodec_channel', 'Original')
    if not config_profile.has_option('FFMPEG MP3 - SETTINGS', 'mp3_vbr'):
        config_profile.set('FFMPEG MP3 - SETTINGS', 'mp3_vbr', '-q:a')
    if not config_profile.has_option('FFMPEG MP3 - SETTINGS', 'mp3_abr'):
        config_profile.set('FFMPEG MP3 - SETTINGS', 'mp3_abr', '')
    if not config_profile.has_option('FFMPEG MP3 - SETTINGS', 'dolbyprologicii'):
        config_profile.set('FFMPEG MP3 - SETTINGS', 'dolbyprologicii', '')
    if not config_profile.has_option('FFMPEG MP3 - SETTINGS', 'ffmpeg_volume'):
        config_profile.set('FFMPEG MP3 - SETTINGS', 'ffmpeg_volume', '0.0')
    if not config_profile.has_option('FFMPEG MP3 - SETTINGS', 'samplerate'):
        config_profile.set('FFMPEG MP3 - SETTINGS', 'samplerate', 'Original')
    if not config_profile.has_option('FFMPEG MP3 - SETTINGS', 'tempo'):
        config_profile.set('FFMPEG MP3 - SETTINGS', 'tempo', 'Original')
    if not config_profile.has_option('FFMPEG MP3 - SETTINGS', 'acodec_bitrate_vbr'):
        config_profile.set('FFMPEG MP3 - SETTINGS', 'acodec_bitrate_vbr', '')
    if not config_profile.has_option('FFMPEG MP3 - SETTINGS', 'acodec_bitrate_cbr_abr'):
        config_profile.set('FFMPEG MP3 - SETTINGS', 'acodec_bitrate_cbr_abr', '')
    # --------------------------------------------------- MP3 Settings
    # QAAC settings --------------------------------------------------- # Create config parameters
    if not config_profile.has_section('FFMPEG QAAC - SETTINGS'):
        config_profile.add_section('FFMPEG QAAC - SETTINGS')
    if not config_profile.has_option('FFMPEG QAAC - SETTINGS', 'q_acodec_profile'):
        config_profile.set('FFMPEG QAAC - SETTINGS', 'q_acodec_profile', 'True VBR')
    if not config_profile.has_option('FFMPEG QAAC - SETTINGS', 'dolbyprologicii'):
        config_profile.set('FFMPEG QAAC - SETTINGS', 'dolbyprologicii', '')
    if not config_profile.has_option('FFMPEG QAAC - SETTINGS', 'acodec_channel'):
        config_profile.set('FFMPEG QAAC - SETTINGS', 'acodec_channel', 'Original')
    if not config_profile.has_option('FFMPEG QAAC - SETTINGS', 'samplerate'):
        config_profile.set('FFMPEG QAAC - SETTINGS', 'samplerate', 'Original')
    if not config_profile.has_option('FFMPEG QAAC - SETTINGS', 'q_acodec_quality'):
        config_profile.set('FFMPEG QAAC - SETTINGS', 'q_acodec_quality', 'High (Default)')
    if not config_profile.has_option('FFMPEG QAAC - SETTINGS', 'q_acodec_quality_amnt'):
        config_profile.set('FFMPEG QAAC - SETTINGS', 'q_acodec_quality_amnt', '109')
    if not config_profile.has_option('FFMPEG QAAC - SETTINGS', 'q_acodec_bitrate'):
        config_profile.set('FFMPEG QAAC - SETTINGS', 'q_acodec_bitrate', '256')
    if not config_profile.has_option('FFMPEG QAAC - SETTINGS', 'q_acodec_gain'):
        config_profile.set('FFMPEG QAAC - SETTINGS', 'q_acodec_gain', '0')
    if not config_profile.has_option('FFMPEG QAAC - SETTINGS', 'qaac_normalize'):
        config_profile.set('FFMPEG QAAC - SETTINGS', 'qaac_normalize', '')
    if not config_profile.has_option('FFMPEG QAAC - SETTINGS', 'qaac_high_efficiency'):
        config_profile.set('FFMPEG QAAC - SETTINGS', 'qaac_high_efficiency', '')
    if not config_profile.has_option('FFMPEG QAAC - SETTINGS', 'qaac_nodither'):
        config_profile.set('FFMPEG QAAC - SETTINGS', 'qaac_nodither', '')
    if not config_profile.has_option('FFMPEG QAAC - SETTINGS', 'qaac_nodelay'):
        config_profile.set('FFMPEG QAAC - SETTINGS', 'qaac_nodelay', '')
    if not config_profile.has_option('FFMPEG QAAC - SETTINGS', 'q_gapless_mode'):
        config_profile.set('FFMPEG QAAC - SETTINGS', 'q_gapless_mode', 'iTunSMPB (Default)')
    if not config_profile.has_option('FFMPEG QAAC - SETTINGS', 'qaac_nooptimize'):
        config_profile.set('FFMPEG QAAC - SETTINGS', 'qaac_nooptimize', '')
    if not config_profile.has_option('FFMPEG QAAC - SETTINGS', 'qaac_threading'):
        config_profile.set('FFMPEG QAAC - SETTINGS', 'qaac_threading', '')
    if not config_profile.has_option('FFMPEG QAAC - SETTINGS', 'qaac_limiter'):
        config_profile.set('FFMPEG QAAC - SETTINGS', 'qaac_limiter', '')
    if not config_profile.has_option('FFMPEG QAAC - SETTINGS', 'tempo'):
        config_profile.set('FFMPEG QAAC - SETTINGS', 'tempo', 'Original')
    # --------------------------------------------------- QAAC Settings
    # FLAC settings --------------------------------------------------- # Create config parameters
    if not config_profile.has_section('FFMPEG FLAC - SETTINGS'):
        config_profile.add_section('FFMPEG FLAC - SETTINGS')
    if not config_profile.has_option('FFMPEG FLAC - SETTINGS', 'acodec_bitrate'):
        config_profile.set('FFMPEG FLAC - SETTINGS', 'acodec_bitrate', 'Level 5 - Default Compression/Speed')
    if not config_profile.has_option('FFMPEG FLAC - SETTINGS', 'acodec_channel'):
        config_profile.set('FFMPEG FLAC - SETTINGS', 'acodec_channel', 'Original')
    if not config_profile.has_option('FFMPEG FLAC - SETTINGS', 'dolbyprologicii'):
        config_profile.set('FFMPEG FLAC - SETTINGS', 'dolbyprologicii', '')
    if not config_profile.has_option('FFMPEG FLAC - SETTINGS', 'volume'):
        config_profile.set('FFMPEG FLAC - SETTINGS', 'volume', '0.0')
    if not config_profile.has_option('FFMPEG FLAC - SETTINGS', 'samplerate'):
        config_profile.set('FFMPEG FLAC - SETTINGS', 'samplerate', 'Original')
    if not config_profile.has_option('FFMPEG FLAC - SETTINGS', 'tempo'):
        config_profile.set('FFMPEG FLAC - SETTINGS', 'tempo', 'Original')
    if not config_profile.has_option('FFMPEG FLAC - SETTINGS', 'flac_lpc_type'):
        config_profile.set('FFMPEG FLAC - SETTINGS', 'flac_lpc_type', 'Default')
    if not config_profile.has_option('FFMPEG FLAC - SETTINGS', 'flac_coefficient'):
        config_profile.set('FFMPEG FLAC - SETTINGS', 'flac_coefficient', '15')
    if not config_profile.has_option('FFMPEG FLAC - SETTINGS', 'flac_lpc_passes'):
        config_profile.set('FFMPEG FLAC - SETTINGS', 'flac_lpc_passes', 'Default')
    # --------------------------------------------------- FLAC Settings
    # ALAC settings --------------------------------------------------- # Create config parameters
    if not config_profile.has_section('FFMPEG ALAC - SETTINGS'):
        config_profile.add_section('FFMPEG ALAC - SETTINGS')
    if not config_profile.has_option('FFMPEG ALAC - SETTINGS', 'acodec_channel'):
        config_profile.set('FFMPEG ALAC - SETTINGS', 'acodec_channel', 'Original')
    if not config_profile.has_option('FFMPEG ALAC - SETTINGS', 'dolbyprologicii'):
        config_profile.set('FFMPEG ALAC - SETTINGS', 'dolbyprologicii', '')
    if not config_profile.has_option('FFMPEG ALAC - SETTINGS', 'volume'):
        config_profile.set('FFMPEG ALAC - SETTINGS', 'volume', '0.0')
    if not config_profile.has_option('FFMPEG ALAC - SETTINGS', 'samplerate'):
        config_profile.set('FFMPEG ALAC - SETTINGS', 'samplerate', 'Original')
    if not config_profile.has_option('FFMPEG ALAC - SETTINGS', 'tempo'):
        config_profile.set('FFMPEG ALAC - SETTINGS', 'tempo', 'Original')
    if not config_profile.has_option('FFMPEG ALAC - SETTINGS', 'alac_min_prediction_order'):
        config_profile.set('FFMPEG ALAC - SETTINGS', 'alac_min_prediction_order', '4')
    if not config_profile.has_option('FFMPEG ALAC - SETTINGS', 'alac_max_prediction_order'):
        config_profile.set('FFMPEG ALAC - SETTINGS', 'alac_max_prediction_order', '6')
    # --------------------------------------------------- ALAC Settings
    # Auto Encode Last Used Options ------------------------------------ # Create config parameters
    if not config_profile.has_section('Auto Encode'):
        config_profile.add_section('Auto Encode')
    if not config_profile.has_option('Auto Encode', 'codec'):
        config_profile.set('Auto Encode', 'codec', '')
    if not config_profile.has_option('Auto Encode', 'command'):
        config_profile.set('Auto Encode', 'command', '')
    # ------------------------------------- Auto Encode Last Used Options
    try:
        with open(config_profile_ini, 'w') as configfile_two:
            config_profile.write(configfile_two)
    except (Exception,):
        messagebox.showinfo(title='Error', message='Could Not Write to profiles.ini file, delete and try again')
    # Profile Config --------------------------------------------------------------------------------------------------
