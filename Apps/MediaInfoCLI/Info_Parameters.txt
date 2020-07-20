General 
Count                     : Count of objects available in this stream
Status                    : Status of bit field (0=IsAccepted, 1=IsFilled, 2=IsUpdated, 3=IsFinished)
StreamCount               : Count of streams of this kind available (base=1)
StreamKind                : Stream type name
StreamKind/String         : Stream type name
StreamKindID              : Stream number (base=0)
StreamKindPos             : Number of the stream, when multiple (base=1)
StreamOrder               : Stream order in the file for type of stream (base=0)
FirstPacketOrder          : Order of the first fully decodable packet met in the file for stream type (base=0)
Inform                    : Last **Inform** call
ID                        : The ID for this stream in this file
ID/String                 : The ID for this stream in this file
OriginalSourceMedium_ID   : The ID for this stream in the original medium of the material
OriginalSourceMedium_ID/S : The ID for this stream in the original medium of the material
UniqueID                  : The unique ID for this stream, should be copied with stream copy
UniqueID/String           : The unique ID for this stream, should be copied with stream copy
MenuID                    : The menu ID for this stream in this file
MenuID/String             : The menu ID for this stream in this file
GeneralCount              : Number of general streams
VideoCount                : Number of video streams
AudioCount                : Number of audio streams
TextCount                 : Number of text streams
OtherCount                : Number of other streams
ImageCount                : Number of image streams
MenuCount                 : Number of menu streams
Video_Format_List         : Video Codecs in this file, separated by /
Video_Format_WithHint_Lis : Video Codecs in this file with popular name (hint), separated by /
Video_Codec_List          : Deprecated, do not use in new projects
Video_Language_List       : Video languages in this file, full names, separated by /
Audio_Format_List         : Audio Codecs in this file,separated by /
Audio_Format_WithHint_Lis : Audio Codecs in this file with popular name (hint), separated by /
Audio_Codec_List          : Deprecated, do not use in new projects
Audio_Language_List       : Audio languages in this file separated by /
Text_Format_List          : Text Codecs in this file, separated by /
Text_Format_WithHint_List : Text Codecs in this file with popular name (hint),separated by /
Text_Codec_List           : Deprecated, do not use in new projects
Text_Language_List        : Text languages in this file, separated by /
Other_Format_List         : Other formats in this file, separated by /
Other_Format_WithHint_Lis : Other formats in this file with popular name (hint), separated by /
Other_Codec_List          : Deprecated, do not use in new projects
Other_Language_List       : Chapters languages in this file, separated by /
Image_Format_List         : Image Codecs in this file, separated by /
Image_Format_WithHint_Lis : Image Codecs in this file with popular name (hint), separated by /
Image_Codec_List          : Deprecated, do not use in new projects
Image_Language_List       : Image languages in this file, separated by /
Menu_Format_List          : Menu Codecs in this file, separated by /
Menu_Format_WithHint_List : Menu Codecs in this file with popular name (hint),separated by /
Menu_Codec_List           : Deprecated, do not use in new projects
Menu_Language_List        : Menu languages in this file, separated by /
CompleteName              : Complete name (Folder+Name+Extension)
FolderName                : Folder name only
FileNameExtension         : File name and extension
FileName                  : File name only
FileExtension             : File extension only
CompleteName_Last         : Complete name (Folder+Name+Extension) of the last file (in the case of a sequence of files)
FolderName_Last           : Folder name only of the last file (in the case of a sequence of files)
FileNameExtension_Last    : File name and extension of the last file (in the case of a sequence of files)
FileName_Last             : File name only of the last file (in the case of a sequence of files)
FileExtension_Last        : File extension only of the last file (in the case of a sequence of files)
Format                    : Format used
Format/String             : Format used + additional features
Format/Info               : Info about this Format
Format/Url                : Link to a description of this format
Format/Extensions         : Known extensions of this format
Format_Commercial         : Commercial name used by vendor for these settings or Format field if there is no difference
Format_Commercial_IfAny   : Commercial name used by vendor for these settings if there is one
Format_Version            : Version of this format
Format_Profile            : Profile of the Format (old XML: 'Profile@Level' format
Format_Level              : Level of the Format (only MIXML)
Format_Compression        : Compression method used
Format_Settings           : Settings needed for decoder used
Format_AdditionalFeatures : Format features needed for fully supporting the content
InternetMediaType         : Internet Media Type (aka MIME Type, Content-Type)
CodecID                   : Codec ID (found in some containers)
CodecID/String            : Codec ID (found in some containers)
CodecID/Info              : Info about this Codec
CodecID/Hint              : A hint/popular name for this Codec
CodecID/Url               : A link to more details about this Codec ID
CodecID_Description       : Manual description given by the container
CodecID_Version           : Version of the CodecID
CodecID_Compatible        : Compatible CodecIDs
Interleaved               : If Audio and video are muxed
Codec                     : Deprecated, do not use in new projects
Codec/String              : Deprecated, do not use in new projects
Codec/Info                : Deprecated, do not use in new projects
Codec/Url                 : Deprecated, do not use in new projects
Codec/Extensions          : Deprecated, do not use in new projects
Codec_Settings            : Deprecated, do not use in new projects
Codec_Settings_Automatic  : Deprecated, do not use in new projects
FileSize                  : File size in bytes
FileSize/String           : File size (with measure)
FileSize/String1          : File size (with measure, 1 digit mini)
FileSize/String2          : File size (with measure, 2 digit mini)
FileSize/String3          : File size (with measure, 3 digit mini)
FileSize/String4          : File size (with measure, 4 digit mini)
Duration                  : Play time of the stream (in ms)
Duration/String           : Play time in format : XXx YYy only, YYy omitted if zero
Duration/String1          : Play time in format : HHh MMmn SSs MMMms, XX omitted if zero
Duration/String2          : Play time in format : XXx YYy only, YYy omitted if zero
Duration/String3          : Play time in format : HH:MM:SS.MMM
Duration/String4          : Play time in format : HH:MM:SS:FF, last colon replaced by semicolon for drop frame if available
Duration/String5          : Play time in format : HH:MM:SS.mmm (HH:MM:SS:FF)
Duration_Start 
Duration_End 
OverallBitRate_Mode       : Bit rate mode of all streams (VBR, CBR)
OverallBitRate_Mode/Strin : Bit rate mode of all streams (Variable, Constant)
OverallBitRate            : Bit rate of all streams (in bps)
OverallBitRate/String     : Bit rate of all streams (with measure)
OverallBitRate_Minimum    : Minimum bit rate (in bps)
OverallBitRate_Minimum/St : Minimum bit rate (with measurement)
OverallBitRate_Nominal    : Nominal bit rate (in bps)
OverallBitRate_Nominal/St : Nominal bit rate (with measurement)
OverallBitRate_Maximum    : Maximum bit rate (in bps)
OverallBitRate_Maximum/St : Maximum bit rate (with measurement)
FrameRate                 : Frames per second
FrameRate/String          : Frames per second (with measurement)
FrameRate_Num             : Frames per second, numerator
FrameRate_Den             : Frames per second, denominator
FrameCount                : Frame count (if a frame contains a count of samples)
Delay                     : Delay fixed in the stream (relative) (in ms)
Delay/String              : Delay with measurement
Delay/String1             : Delay with measurement
Delay/String2             : Delay with measurement
Delay/String3             : format : HH:MM:SS.MMM
Delay/String4             : Delay in format : HH:MM:SS:FF, last colon replaced by semicolon for drop frame if available
Delay/String5             : Delay in format : HH:MM:SS.mmm (HH:MM:SS:FF)
Delay_Settings            : Delay settings (in case of timecode, for example)
Delay_DropFrame           : Delay drop frame
Delay_Source              : Delay source (Container, Stream, empty)
Delay_Source/String       : Delay source (Container, Stream, empty)
StreamSize                : Stream size (in bytes)
StreamSize/String 
StreamSize/String1 
StreamSize/String2 
StreamSize/String3 
StreamSize/String4 
StreamSize/String5        : Stream size with proportion
StreamSize_Proportion     : Stream size divided by file size
StreamSize_Demuxed        : StreamSize after demux (in bytes)
StreamSize_Demuxed/String : StreamSize_Demuxed with percentage value
StreamSize_Demuxed/String1 
StreamSize_Demuxed/String2 
StreamSize_Demuxed/String3 
StreamSize_Demuxed/String4 
StreamSize_Demuxed/String : StreamSize_Demuxed with percentage value (note: theoretical value, not for real use)
HeaderSize 
DataSize 
FooterSize 
IsStreamable 
Album_ReplayGain_Gain     : The gain to apply to reach 89dB SPL on playback
Album_ReplayGain_Gain/String 
Album_ReplayGain_Peak     : The maximum absolute peak value of the item
Encryption 
Encryption_Format 
Encryption_Length 
Encryption_Method 
Encryption_Mode 
Encryption_Padding 
Encryption_InitializationVector 
UniversalAdID/String      : Universal Ad-ID, see https://ad-id.org
UniversalAdID_Registry    : Universal Ad-ID registry
UniversalAdID_Value       : Universal Ad-ID value
Title                     : (Generic)Title of file
Title_More                : (Generic)More info about the title of file
Title/Url                 : (Generic)Url
Domain                    : Universe movies belong to, e.g. Star Wars, Stargate, Buffy, Dragonball
Collection                : Name of the series, e.g. Star Wars movies, Stargate SG-1, Stargate Atlantis, Buffy, Angel
Season                    : Name of the season, e.g. Star Wars first Trilogy, Season 1
Season_Position           : Number of the Season
Season_Position_Total     : Place of the season, e.g. 2 of 7
Movie                     : Name of the movie. Eg : Star Wars, A New Hope
Movie_More                : More info about the movie
Movie/Country             : Country, where the movie was produced
Movie/Url                 : Homepage for the movie
Album                     : Name of an audio-album. Eg : The Joshua Tree
Album_More                : More info about the album
Album/Sort 
Album/Performer           : Album performer/artist of this file
Album/Performer/Sort 
Album/Performer/Url       : Homepage of the album performer/artist
Comic                     : Name of the comic.
Comic_More                : More info about the comic
Comic/Position_Total      : Place of the comic, e.g. 1 of 10
Part                      : Name of the part. e.g. CD1, CD2
Part/Position             : Number of the part
Part/Position_Total       : Place of the part e.g. 2 of 3
Track                     : Name of the track. e.g. track 1, track 2
Track_More                : More info about the track
Track/Url                 : Link to a site about this track
Track/Sort 
Track/Position            : Number of this track
Track/Position_Total      : Place of this track, e.g. 3 of 15
PackageName               : Package name i.e. technical flavor of the content
Grouping                  : iTunes grouping
Chapter                   : Name of the chapter
SubTrack                  : Name of the subtrack
Original/Album            : Original name of the album
Original/Movie            : Original name of the movie
Original/Part             : Original name of the part
Original/Track            : Original name of the track
Compilation               : iTunes compilation
Compilation/String        : iTunes compilation
Performer                 : Main performer(s)/artist(s)
Performer/Sort 
Performer/Url             : Homepage of the performer/artist
Original/Performer        : Original artist(s)/performer(s)
Accompaniment             : Band/orchestra/accompaniment/musician
Composer                  : Name of the original composer
Composer/Nationality      : Nationality of the primary composer of the piece (mostly for classical music)
Composer/Sort 
Arranger                  : The person who arranged the piece (e.g. Ravel)
Lyricist                  : The person who wrote the lyrics for the piece
Original/Lyricist         : Original lyricist(s)/text writer(s).
Conductor                 : The artist(s) who performed the work. In classical music this would be the conductor, orchestra, soloists, etc.
Director                  : Name of the director
CoDirector                : Name of the codirector
AssistantDirector         : Name of the assistant director
DirectorOfPhotography     : Name of the director of photography, also known as cinematographer
SoundEngineer             : Name of the sound engineer or sound recordist
ArtDirector               : Name of the person who oversees the artists and craftspeople who build the sets
ProductionDesigner        : Name of the person responsible for designing the overall visual appearance of a movie
Choreographer             : Name of the choreographer
CostumeDesigner           : Name of the costume designer
Actor                     : Real name of an actor/actress playing a role in the movie
Actor_Character           : Name of the character an actor or actress plays in this movie
WrittenBy                 : Author of the story or script
ScreenplayBy              : Author of the screenplay or scenario (used for movies and TV shows)
EditedBy                  : Editors name
CommissionedBy            : Name of the person or organization that commissioned the subject of the file
Producer                  : Name of the producer of the movie
CoProducer                : Name of a co-producer
ExecutiveProducer         : Name of an executive producer
MusicBy                   : Main musical artist for a movie
DistributedBy             : Company responsible for distribution of the content
OriginalSourceForm/Distri : Name of the person or organization who supplied the original subject
MasteredBy                : The engineer who mastered the content for a physical medium or for digital distribution
EncodedBy                 : Name of the person/organisation that encoded/ripped the audio file.
RemixedBy                 : Name of the artist(s) that interpreted, remixed, or otherwise modified the content
ProductionStudio          : Main production studio
ThanksTo                  : A very general tag for everyone else that wants to be listed
Publisher                 : Name of the organization publishing the album (i.e. the 'record label') or movie
Publisher/URL             : Publisher's official webpage
Label                     : Brand or trademark associated with the marketing of music recordings and music videos
Genre                     : Main genre of the audio or video. e.g. classical, ambient-house, synthpop, sci-fi, drama, etc.
PodcastCategory           : Podcast category
Mood                      : Intended to reflect the mood of the item with a few keywords, e.g. Romantic, Sad, Uplifting, etc.
ContentType               : The type or genre of the content. e.g. Documentary, Feature Film, Cartoon, Music Video, Music, Sound FX, etc.
Subject                   : Describes the topic of the file, such as 'Aerial view of Seattle.'
Description               : A short description of the contents, such as 'Two birds flying.'
Keywords                  : Keywords for the content separated by a comma, used for searching
Summary                   : Plot outline or a summary of the story
Synopsis                  : Description of the story line of the item
Period                    : Describes the period that the piece is from or about. e.g. Renaissance.
LawRating                 : Legal rating of a movie. Format depends on country of origin (e.g. PG or R in the USA, an age in other countries or a URI defining a logo)
LawRating_Reason          : Reason for the law rating
ICRA                      : The ICRA rating (previously RSACi)
Released_Date             : Date/year that the content was released
Original/Released_Date    : Date/year that the content was originally released
Recorded_Date             : Time/date/year that the recording began
Encoded_Date              : Time/date/year that the encoding of this content was completed
Tagged_Date               : Time/date/year that the tags were added to this content
Written_Date              : Time/date/year that the composition of the music/script began
Mastered_Date             : Time/date/year that the content was transferred to a digital medium.
File_Created_Date         : Time that the file was created on the file system
File_Created_Date_Local   : Time that the file was created on the file system (Warning: this field depends of local configuration, do not use it in an international database)
File_Modified_Date        : Time that the file was last modified on the file system
File_Modified_Date_Local  : Time that the file was last modified on the file system (Warning: this field depends of local configuration, do not use it in an international database)
Recorded_Location         : Location where track was recorded (See COMPOSITION_LOCATION for format)
Written_Location          : Location that the item was originally designed/written. Information should be stored in the following format: country code, state/province, city where the country code is the same 2 octets as in Internet domains, or possibly ISO-3166. e.g. US, Texas, Austin or US, , Austin.
Archival_Location         : Location where an item is archived (e.g. Louvre, Paris, France)
Encoded_Application       : Name of the software package used to create the file, such as Microsoft WaveEdiTY
Encoded_Application/Strin : Name of the software package used to create the file, such as Microsoft WaveEdit, trying to have the format 'CompanyName ProductName (OperatingSystem) Version (Date)'
Encoded_Application_Compa : Name of the company of the encoding application
Encoded_Application_Name  : Name of the encoding product
Encoded_Application_Versi : Version of the encoding product
Encoded_Application_Url   : URL associated with the encoding software
Encoded_Library           : Software used to create the file
Encoded_Library/String    : Software used to create the file, trying to have the format 'CompanyName ProductName (OperatingSystem) Version (Date)'
Encoded_Library_CompanyNa : Name of the company
Encoded_Library_Name      : Name of the the encoding library
Encoded_Library_Version   : Version of encoding library
Encoded_Library_Date      : Release date of encoding library
Encoded_Library_Settings  : Parameters used by the encoding library
Encoded_OperatingSystem   : Operating System used by encoding application
Cropped                   : Describes whether an image has been cropped and, if so, how it was cropped
Dimensions                : Specifies the size of the original subject of the file (e.g. 8.5 in h, 11 in w)
DotsPerInch               : Stores dots per inch setting of the digitization mechanism used to produce the file
Lightness                 : Describes the changes in lightness settings on the digitization mechanism made during the production of the file
OriginalSourceMedium      : Original medium of the material (e.g. vinyl, Audio-CD, Super8 or BetaMax)
OriginalSourceForm        : Original form of the material (e.g. slide, paper, map)
OriginalSourceForm/NumCol : Number of colors requested when digitizing (e.g. 256 for images or 32 bit RGB for video)
OriginalSourceForm/Name   : Name of the product the file was originally intended for
OriginalSourceForm/Croppe : Describes whether the original image has been cropped and, if so, how it was cropped (e.g. 16:9 to 4:3, top and bottom)
OriginalSourceForm/Sharpn : Identifies changes in sharpness the digitization mechanism made during the production of the file
Tagged_Application        : Software used to tag the file
BPM                       : Average number of beats per minute
ISRC                      : International Standard Recording Code, excluding the ISRC prefix and including hyphens
ISBN                      : International Standard Book Number.
BarCode                   : EAN-13 (13-digit European Article Numbering) or UPC-A (12-digit Universal Product Code) bar code identifier
LCCN                      : Library of Congress Control Number
CatalogNumber             : A label-specific catalogue number used to identify the release. e.g. TIC 01
LabelCode                 : A 4-digit or 5-digit number to identify the record label, typically printed as (LC) xxxx or (LC) 0xxxx on CDs medias or covers, with only the number being stored
Owner                     : Owner of the file
Copyright                 : Copyright attribution
Copyright/Url             : Link to a site with copyright/legal information
Producer_Copyright        : Copyright information as per the production copyright holder
TermsOfUse                : License information (e.g. All Rights Reserved, Any Use Permitted)
ServiceName 
ServiceChannel 
Service/Url 
ServiceProvider 
ServiceProvider/Url 
ServiceType 
NetworkName 
OriginalNetworkName 
Country 
TimeZone 
Cover                     : Is there a cover
Cover_Description         : Short description (e.g. Earth in space)
Cover_Type 
Cover_Mime                : Mime type of cover file
Cover_Data                : Cover, in binary format, encoded as BASE64
Lyrics                    : Text of a song
Comment                   : Any comment related to the content
Rating                    : A numeric value defining how much a person likes the song/movie. The number is between 0 and 5 with decimal values possible (e.g. 2.7), 5(.0) being the highest possible rating.
Added_Date                : Date/year the item was added to the owners collection
Played_First_Date         : Date the owner first played an item
Played_Last_Date          : Date the owner last played an item
Played_Count              : Number of times an item was played
EPG_Positions_Begin 
EPG_Positions_End 
 
Video 
Count                     : Count of objects available in this stream
Status                    : bit field (0=IsAccepted, 1=IsFilled, 2=IsUpdated, 3=IsFinished)
StreamCount               : Count of streams of that kind available
StreamKind                : Stream type name
StreamKind/String         : Stream type name
StreamKindID              : Number of the stream (base=0)
StreamKindPos             : When multiple streams, number of the stream (base=1)
StreamOrder               : Stream order in the file, whatever is the kind of stream (base=0)
FirstPacketOrder          : Order of the first fully decodable packet met in the file, whatever is the kind of stream (base=0)
Inform                    : Last **Inform** call
ID                        : The ID for this stream in this file
ID/String                 : The ID for this stream in this file
OriginalSourceMedium_ID   : The ID for this stream in the original medium of the material
OriginalSourceMedium_ID/S : The ID for this stream in the original medium of the material
UniqueID                  : The unique ID for this stream, should be copied with stream copy
UniqueID/String           : The unique ID for this stream, should be copied with stream copy
MenuID                    : The menu ID for this stream in this file
MenuID/String             : The menu ID for this stream in this file
Format                    : Format used
Format/String             : Format used + additional features
Format/Info               : Info about Format
Format/Url                : Link
Format_Commercial         : Commercial name used by vendor for theses setings or Format field if there is no difference
Format_Commercial_IfAny   : Commercial name used by vendor for theses setings if there is one
Format_Version            : Version of this format
Format_Profile            : Profile of the Format (old XML: 'Profile@Level@Tier' format
Format_Level              : Level of the Format (only MIXML)
Format_Tier               : Tier of the Format (only MIXML)
Format_Compression        : Compression method used
Format_AdditionalFeatures : Format features needed for fully supporting the content
MultiView_BaseProfile     : Multiview, profile of the base stream
MultiView_Count           : Multiview, count of views
MultiView_Layout          : Multiview, how views are muxed in the container in case of it is not muxing in the stream
HDR_Format                : Format used
HDR_Format/String         : Format used + version + profile + level + layers + settings + compatibility
HDR_Format_Commercial     : Commercial name used by vendor for theses HDR settings or HDR Format field if there is no difference
HDR_Format_Version        : Version of this format
HDR_Format_Profile        : Profile of the Format
HDR_Format_Level          : Level of the Format
HDR_Format_Settings       : Settings of the Format
HDR_Format_Compatibility  : Compatibility with some commercial namings
Format_Settings           : Settings needed for decoder used, summary
Format_Settings_BVOP      : Settings needed for decoder used, detailled
Format_Settings_BVOP/Stri : Settings needed for decoder used, detailled
Format_Settings_QPel      : Settings needed for decoder used, detailled
Format_Settings_QPel/Stri : Settings needed for decoder used, detailled
Format_Settings_GMC       : Settings needed for decoder used, detailled
Format_Settings_GMC/String 
Format_Settings_Matrix    : Settings needed for decoder used, detailled
Format_Settings_Matrix/St : Settings needed for decoder used, detailled
Format_Settings_Matrix_Da : Matrix, in binary format encoded BASE64. Order = intra, non-intra, gray intra, gray non-intra
Format_Settings_CABAC     : Settings needed for decoder used, detailled
Format_Settings_CABAC/Str : Settings needed for decoder used, detailled
Format_Settings_RefFrames : Settings needed for decoder used, detailled
Format_Settings_RefFrames : Settings needed for decoder used, detailled
Format_Settings_Pulldown  : Settings needed for decoder used, detailled
Format_Settings_Endianness 
Format_Settings_Packing 
Format_Settings_FrameMode : Settings needed for decoder used, detailled
Format_Settings_GOP       : Settings needed for decoder used, detailled (M=x N=y)
Format_Settings_PictureSt : Settings needed for decoder used, detailled (Type of frame, and field/frame info)
Format_Settings_Wrapping  : Wrapping mode (Frame wrapped or Clip wrapped)
InternetMediaType         : Internet Media Type (aka MIME Type, Content-Type)
MuxingMode                : How this file is muxed in the container
CodecID                   : Codec ID (found in some containers)
CodecID/String            : Codec ID (found in some containers)
CodecID/Info              : Info on the codec
CodecID/Hint              : Hint/popular name for this codec
CodecID/Url               : Homepage for more details about this codec
CodecID_Description       : Manual description given by the container
Codec                     : Deprecated, do not use in new projects
Codec/String              : Deprecated, do not use in new projects
Codec/Family              : Deprecated, do not use in new projects
Codec/Info                : Deprecated, do not use in new projects
Codec/Url                 : Deprecated, do not use in new projects
Codec/CC                  : Deprecated, do not use in new projects
Codec_Profile             : Deprecated, do not use in new projects
Codec_Description         : Deprecated, do not use in new projects
Codec_Settings            : Deprecated, do not use in new projects
Codec_Settings_PacketBitS : Deprecated, do not use in new projects
Codec_Settings_BVOP       : Deprecated, do not use in new projects
Codec_Settings_QPel       : Deprecated, do not use in new projects
Codec_Settings_GMC        : Deprecated, do not use in new projects
Codec_Settings_GMC/String : Deprecated, do not use in new projects
Codec_Settings_Matrix     : Deprecated, do not use in new projects
Codec_Settings_Matrix_Dat : Deprecated, do not use in new projects
Codec_Settings_CABAC      : Deprecated, do not use in new projects
Codec_Settings_RefFrames  : Deprecated, do not use in new projects
Duration                  : Play time of the stream in ms
Duration/String           : Play time in format : XXx YYy only, YYy omited if zero
Duration/String1          : Play time in format : HHh MMmn SSs MMMms, XX omited if zero
Duration/String2          : Play time in format : XXx YYy only, YYy omited if zero
Duration/String3          : Play time in format : HH:MM:SS.MMM
Duration/String4          : Play time in format : HH:MM:SS:FF, last colon replaced by semicolon for drop frame if available
Duration/String5          : Play time in format : HH:MM:SS.mmm (HH:MM:SS:FF)
Duration_FirstFrame       : Duration of the first frame if it is longer than others, in ms
Duration_FirstFrame/Strin : Duration of the first frame if it is longer than others, in format : XXx YYy only, YYy omited if zero
Duration_FirstFrame/Strin : Duration of the first frame if it is longer than others, in format : HHh MMmn SSs MMMms, XX omited if zero
Duration_FirstFrame/Strin : Duration of the first frame if it is longer than others, in format : XXx YYy only, YYy omited if zero
Duration_FirstFrame/Strin : Duration of the first frame if it is longer than others, in format : HH:MM:SS.MMM
Duration_FirstFrame/Strin : Play time in format : HH:MM:SS:FF, last colon replaced by semicolon for drop frame if available
Duration_FirstFrame/Strin : Play time in format : HH:MM:SS.mmm (HH:MM:SS:FF)
Duration_LastFrame        : Duration of the last frame if it is longer than others, in ms
Duration_LastFrame/String : Duration of the last frame if it is longer than others, in format : XXx YYy only, YYy omited if zero
Duration_LastFrame/String : Duration of the last frame if it is longer than others, in format : HHh MMmn SSs MMMms, XX omited if zero
Duration_LastFrame/String : Duration of the last frame if it is longer than others, in format : XXx YYy only, YYy omited if zero
Duration_LastFrame/String : Duration of the last frame if it is longer than others, in format : HH:MM:SS.MMM
Duration_LastFrame/String : Play time in format : HH:MM:SS:FF, last colon replaced by semicolon for drop frame if available
Duration_LastFrame/String : Play time in format : HH:MM:SS.mmm (HH:MM:SS:FF)
Source_Duration           : Source Play time of the stream, in ms
Source_Duration/String    : Source Play time in format : XXx YYy only, YYy omited if zero
Source_Duration/String1   : Source Play time in format : HHh MMmn SSs MMMms, XX omited if zero
Source_Duration/String2   : Source Play time in format : XXx YYy only, YYy omited if zero
Source_Duration/String3   : Source Play time in format : HH:MM:SS.MMM
Source_Duration/String4   : Play time in format : HH:MM:SS:FF, last colon replaced by semicolon for drop frame if available
Source_Duration/String5   : Play time in format : HH:MM:SS.mmm (HH:MM:SS:FF)
Source_Duration_FirstFram : Source Duration of the first frame if it is longer than others, in ms
Source_Duration_FirstFram : Source Duration of the first frame if it is longer than others, in format : XXx YYy only, YYy omited if zero
Source_Duration_FirstFram : Source Duration of the first frame if it is longer than others, in format : HHh MMmn SSs MMMms, XX omited if zero
Source_Duration_FirstFram : Source Duration of the first frame if it is longer than others, in format : XXx YYy only, YYy omited if zero
Source_Duration_FirstFram : Source Duration of the first frame if it is longer than others, in format : HH:MM:SS.MMM
Source_Duration_FirstFram : Play time in format : HH:MM:SS:FF, last colon replaced by semicolon for drop frame if available
Source_Duration_FirstFram : Play time in format : HH:MM:SS.mmm (HH:MM:SS:FF)
Source_Duration_LastFrame : Source Duration of the last frame if it is longer than others, in ms
Source_Duration_LastFrame : Source Duration of the last frame if it is longer than others, in format : XXx YYy only, YYy omited if zero
Source_Duration_LastFrame : Source Duration of the last frame if it is longer than others, in format : HHh MMmn SSs MMMms, XX omited if zero
Source_Duration_LastFrame : Source Duration of the last frame if it is longer than others, in format : XXx YYy only, YYy omited if zero
Source_Duration_LastFrame : Source Duration of the last frame if it is longer than others, in format : HH:MM:SS.MMM
Source_Duration_LastFrame : Play time in format : HH:MM:SS:FF, last colon replaced by semicolon for drop frame if available
Source_Duration_LastFrame : Play time in format : HH:MM:SS.mmm (HH:MM:SS:FF)
BitRate_Mode              : Bit rate mode (VBR, CBR)
BitRate_Mode/String       : Bit rate mode (Variable, Cconstant)
BitRate                   : Bit rate in bps
BitRate/String            : Bit rate (with measurement)
BitRate_Minimum           : Minimum Bit rate in bps
BitRate_Minimum/String    : Minimum Bit rate (with measurement)
BitRate_Nominal           : Nominal Bit rate in bps
BitRate_Nominal/String    : Nominal Bit rate (with measurement)
BitRate_Maximum           : Maximum Bit rate in bps
BitRate_Maximum/String    : Maximum Bit rate (with measurement)
BitRate_Encoded           : Encoded (with forced padding) bit rate in bps, if some container padding is present
BitRate_Encoded/String    : Encoded (with forced padding) bit rate (with measurement), if some container padding is present
Width                     : Width (aperture size if present) in pixel
Width/String              : Width (aperture size if present) with measurement (pixel)
Width_Offset              : Offset between original width and displayed width in pixel
Width_Offset/String       : Offset between original width and displayed width in pixel
Width_Original            : Original (in the raw stream) width in pixel
Width_Original/String     : Original (in the raw stream) width with measurement (pixel)
Width_CleanAperture       : Clean Aperture width in pixel
Width_CleanAperture/Strin : Clean Aperture width with measurement (pixel)
Height                    : Height in pixel
Height/String             : Height with measurement (pixel)
Height_Offset             : Offset between original height and displayed height in pixel
Height_Offset/String      : Offset between original height and displayed height  in pixel
Height_Original           : Original (in the raw stream) height in pixel
Height_Original/String    : Original (in the raw stream) height with measurement (pixel)
Height_CleanAperture      : Clean Aperture height in pixel
Height_CleanAperture/Stri : Clean Aperture height with measurement (pixel)
Stored_Width              : Stored width
Stored_Height             : Stored height
Sampled_Width             : Sampled width
Sampled_Height            : Sampled height
PixelAspectRatio          : Pixel Aspect ratio
PixelAspectRatio/String   : Pixel Aspect ratio
PixelAspectRatio_Original : Original (in the raw stream) Pixel Aspect ratio
PixelAspectRatio_Original : Original (in the raw stream) Pixel Aspect ratio
PixelAspectRatio_CleanApe : Clean Aperture Pixel Aspect ratio
PixelAspectRatio_CleanApe : Clean Aperture Pixel Aspect ratio
DisplayAspectRatio        : Display Aspect ratio
DisplayAspectRatio/String : Display Aspect ratio
DisplayAspectRatio_Origin : Original (in the raw stream) Display Aspect ratio
DisplayAspectRatio_Origin : Original (in the raw stream) Display Aspect ratio
DisplayAspectRatio_CleanA : Clean Aperture Display Aspect ratio
DisplayAspectRatio_CleanA : Clean Aperture Display Aspect ratio
ActiveFormatDescription   : Active Format Description (AFD value)
ActiveFormatDescription/S : Active Format Description (text)
ActiveFormatDescription_M : Active Format Description (AFD value) muxing mode (Ancillary or Raw stream)
Rotation                  : Rotation
Rotation/String           : Rotation (if not horizontal)
FrameRate_Mode            : Frame rate mode (CFR, VFR)
FrameRate_Mode/String     : Frame rate mode (Constant, Variable)
FrameRate_Mode_Original   : Original frame rate mode (CFR, VFR)
FrameRate_Mode_Original/S : Original frame rate mode (Constant, Variable)
FrameRate                 : Frames per second
FrameRate/String          : Frames per second (with measurement)
FrameRate_Num             : Frames per second, numerator
FrameRate_Den             : Frames per second, denominator
FrameRate_Minimum         : Minimum Frames per second
FrameRate_Minimum/String  : Minimum Frames per second (with measurement)
FrameRate_Nominal         : Nominal Frames per second
FrameRate_Nominal/String  : Nominal Frames per second (with measurement)
FrameRate_Maximum         : Maximum Frames per second
FrameRate_Maximum/String  : Maximum Frames per second (with measurement)
FrameRate_Original        : Original (in the raw stream) frames per second
FrameRate_Original/String : Original (in the raw stream) frames per second (with measurement)
FrameRate_Original_Num    : Frames per second, numerator
FrameRate_Original_Den    : Frames per second, denominator
FrameCount                : Number of frames
Source_FrameCount         : Source Number of frames
Standard                  : NTSC or PAL
Resolution                : Deprecated, do not use in new projects
Resolution/String         : Deprecated, do not use in new projects
Colorimetry               : Deprecated, do not use in new projects
ColorSpace 
ChromaSubsampling 
ChromaSubsampling/String 
ChromaSubsampling_Position 
BitDepth                  : 16/24/32
BitDepth/String           : 16/24/32 bits
ScanType 
ScanType/String 
ScanType_Original 
ScanType_Original/String 
ScanType_StoreMethod 
ScanType_StoreMethod_FieldsPerBlock 
ScanType_StoreMethod/String 
ScanOrder 
ScanOrder/String 
ScanOrder_Stored 
ScanOrder_Stored/String 
ScanOrder_StoredDisplayedInverted 
ScanOrder_Original 
ScanOrder_Original/String 
Interlacement             : Deprecated, do not use in new projects
Interlacement/String      : Deprecated, do not use in new projects
Compression_Mode          : Compression mode (Lossy or Lossless)
Compression_Mode/String   : Compression mode (Lossy or Lossless)
Compression_Ratio         : Current stream size divided by uncompressed stream size
Bits-(Pixel*Frame)        : bits/(Pixel*Frame) (like Gordian Knot)
Delay                     : Delay fixed in the stream (relative) IN MS
Delay/String              : Delay with measurement
Delay/String1             : Delay with measurement
Delay/String2             : Delay with measurement
Delay/String3             : Delay in format : HH:MM:SS.MMM
Delay/String4             : Delay in format : HH:MM:SS:FF, last colon replaced by semicolon for drop frame if available
Delay/String5             : Delay in format : HH:MM:SS.mmm (HH:MM:SS:FF)
Delay_Settings            : Delay settings (in case of timecode for example)
Delay_DropFrame           : Delay drop frame
Delay_Source              : Delay source (Container or Stream or empty)
Delay_Source/String       : Delay source (Container or Stream or empty)
Delay_Original            : Delay fixed in the raw stream (relative) IN MS
Delay_Original/String     : Delay with measurement
Delay_Original/String1    : Delay with measurement
Delay_Original/String2    : Delay with measurement
Delay_Original/String3    : Delay in format: HH:MM:SS.MMM
Delay_Original/String4    : Delay in format: HH:MM:SS:FF, last colon replaced by semicolon for drop frame if available
Delay_Original/String5    : Delay in format : HH:MM:SS.mmm (HH:MM:SS:FF)
Delay_Original_Settings   : Delay settings (in case of timecode for example)
Delay_Original_DropFrame  : Delay drop frame info
Delay_Original_Source     : Delay source (Stream or empty)
TimeStamp_FirstFrame      : TimeStamp fixed in the stream (relative) IN MS
TimeStamp_FirstFrame/Stri : TimeStamp with measurement
TimeStamp_FirstFrame/Stri : TimeStamp with measurement
TimeStamp_FirstFrame/Stri : TimeStamp with measurement
TimeStamp_FirstFrame/Stri : TimeStamp in format : HH:MM:SS.MMM
TimeStamp_FirstFrame/Stri : TimeStamp in format: HH:MM:SS:FF, last colon replaced by semicolon for drop frame if available
TimeStamp_FirstFrame/Stri : TimeStamp in format : HH:MM:SS.mmm (HH:MM:SS:FF)
TimeCode_FirstFrame       : Time code in HH:MM:SS:FF, last colon replaced by semicolon for drop frame if available format
TimeCode_Settings         : Time code settings
TimeCode_Source           : Time code source (Container, Stream, SystemScheme1, SDTI, ANC...)
Gop_OpenClosed            : Time code information about Open/Closed
Gop_OpenClosed/String     : Time code information about Open/Closed
Gop_OpenClosed_FirstFrame : Time code information about Open/Closed of first frame if GOP is Open for the other GOPs
Gop_OpenClosed_FirstFrame : Time code information about Open/Closed of first frame if GOP is Open for the other GOPs
StreamSize                : Streamsize in bytes
StreamSize/String         : Streamsize in with percentage value
StreamSize/String1 
StreamSize/String2 
StreamSize/String3 
StreamSize/String4 
StreamSize/String5        : Streamsize in with percentage value
StreamSize_Proportion     : Stream size divided by file size
StreamSize_Demuxed        : StreamSize in bytes of hte stream after demux
StreamSize_Demuxed/String : StreamSize_Demuxed in with percentage value
StreamSize_Demuxed/String1 
StreamSize_Demuxed/String2 
StreamSize_Demuxed/String3 
StreamSize_Demuxed/String4 
StreamSize_Demuxed/String : StreamSize_Demuxed in with percentage value (note: theoritical value, not for real use)
Source_StreamSize         : Source Streamsize in bytes
Source_StreamSize/String  : Source Streamsize in with percentage value
Source_StreamSize/String1 
Source_StreamSize/String2 
Source_StreamSize/String3 
Source_StreamSize/String4 
Source_StreamSize/String5 : Source Streamsize in with percentage value
Source_StreamSize_Proport : Source Stream size divided by file size
StreamSize_Encoded        : Encoded Streamsize in bytes
StreamSize_Encoded/String : Encoded Streamsize in with percentage value
StreamSize_Encoded/String1 
StreamSize_Encoded/String2 
StreamSize_Encoded/String3 
StreamSize_Encoded/String4 
StreamSize_Encoded/String : Encoded Streamsize in with percentage value
StreamSize_Encoded_Propor : Encoded Stream size divided by file size
Source_StreamSize_Encoded : Source Encoded Streamsize in bytes
Source_StreamSize_Encoded : Source Encoded Streamsize in with percentage value
Source_StreamSize_Encoded/String1 
Source_StreamSize_Encoded/String2 
Source_StreamSize_Encoded/String3 
Source_StreamSize_Encoded/String4 
Source_StreamSize_Encoded : Source Encoded Streamsize in with percentage value
Source_StreamSize_Encoded : Source Encoded Stream size divided by file size
Alignment                 : How this stream file is aligned in the container
Alignment/String 
Title                     : Name of the track
Encoded_Application       : Name of the software package used to create the file, such as Microsoft WaveEdit
Encoded_Application/Strin : Name of the software package used to create the file, such as Microsoft WaveEdit, trying to have the format 'CompanyName ProductName (OperatingSystem) Version (Date)'
Encoded_Application_Compa : Name of the company
Encoded_Application_Name  : Name of the product
Encoded_Application_Versi : Version of the product
Encoded_Application_Url   : Name of the software package used to create the file, such as Microsoft WaveEdit.
Encoded_Library           : Software used to create the file
Encoded_Library/String    : Software used to create the file, trying to have the format 'CompanyName ProductName (OperatingSystem) Version (Date)'
Encoded_Library_CompanyNa : Name of the company
Encoded_Library_Name      : Name of the the encoding-software
Encoded_Library_Version   : Version of encoding-software
Encoded_Library_Date      : Release date of software
Encoded_Library_Settings  : Parameters used by the software
Encoded_OperatingSystem   : Operating System of encoding-software
Language                  : Language (2-letter ISO 639-1 if exists, else 3-letter ISO 639-2, and with optional ISO 3166-1 country separated by a dash if available, e.g. en, en-us, zh-cn)
Language/String           : Language (full)
Language/String1          : Language (full)
Language/String2          : Language (2-letter ISO 639-1 if exists, else empty)
Language/String3          : Language (3-letter ISO 639-2 if exists, else empty)
Language/String4          : Language (2-letter ISO 639-1 if exists with optional ISO 3166-1 country separated by a dash if available, e.g. en, en-us, zh-cn, else empty)
Language_More             : More info about Language (e.g. Director's Comment)
ServiceKind               : Service kind, e.g. visually impaired, commentary, voice over
ServiceKind/String        : Service kind (full)
Disabled                  : Set if that track should not be used
Disabled/String           : Set if that track should not be used
Default                   : Set if that track should be used if no language found matches the user preference.
Default/String            : Set if that track should be used if no language found matches the user preference.
Forced                    : Set if that track should be used if no language found matches the user preference.
Forced/String             : Set if that track should be used if no language found matches the user preference.
AlternateGroup            : Number of a group in order to provide versions of the same track
AlternateGroup/String     : Number of a group in order to provide versions of the same track
Encoded_Date              : UTC time that the encoding of this item was completed began.
Tagged_Date               : UTC time that the tags were done for this item.
Encryption 
BufferSize                : Defines the size of the buffer needed to decode the sequence.
colour_description_presen : Presence of colour description
colour_description_presen : Presence of colour description (source)
colour_description_presen : Presence of colour description (if incoherencies)
colour_description_presen : Presence of colour description (source if incoherencies)
colour_range              : Colour range for YUV colour space
colour_range_Source       : Colour range for YUV colour space (source)
colour_range_Original     : Colour range for YUV colour space (if incoherencies)
colour_range_Original_Sou : Colour range for YUV colour space (source if incoherencies)
colour_primaries          : Chromaticity coordinates of the source primaries
colour_primaries_Source   : Chromaticity coordinates of the source primaries (source)
colour_primaries_Original : Chromaticity coordinates of the source primaries (if incoherencies)
colour_primaries_Original : Chromaticity coordinates of the source primaries (source if incoherencies)
transfer_characteristics  : Opto-electronic transfer characteristic of the source picture
transfer_characteristics_ : Opto-electronic transfer characteristic of the source picture (source)
transfer_characteristics_ : Opto-electronic transfer characteristic of the source picture (if incoherencies)
transfer_characteristics_ : Opto-electronic transfer characteristic of the source picture (source if incoherencies)
matrix_coefficients       : Matrix coefficients used in deriving luma and chroma signals from the green, blue, and red primaries
matrix_coefficients_Sourc : Matrix coefficients used in deriving luma and chroma signals from the green, blue, and red primaries (source)
matrix_coefficients_Origi : Matrix coefficients used in deriving luma and chroma signals from the green, blue, and red primaries (if incoherencies)
matrix_coefficients_Origi : Matrix coefficients used in deriving luma and chroma signals from the green, blue, and red primaries (source if incoherencies)
MasteringDisplay_ColorPri : Chromaticity coordinates of the source primaries of the mastering display
MasteringDisplay_ColorPri : Chromaticity coordinates of the source primaries of the mastering display (source)
MasteringDisplay_ColorPri : Chromaticity coordinates of the source primaries of the mastering display (if incoherencies)
MasteringDisplay_ColorPri : Chromaticity coordinates of the source primaries of the mastering display (source if incoherencies)
MasteringDisplay_Luminanc : Luminance of the mastering display
MasteringDisplay_Luminanc : Luminance of the mastering display (source)
MasteringDisplay_Luminanc : Luminance of the mastering display (if incoherencies)
MasteringDisplay_Luminanc : Luminance of the mastering display (source if incoherencies)
MaxCLL                    : Maximum content light level
MaxCLL_Source             : Maximum content light level (source)
MaxCLL_Original           : Maximum content light level (if incoherencies)
MaxCLL_Original_Source    : Maximum content light level (source if incoherencies)
MaxFALL                   : Maximum frame average light level
MaxFALL_Source            : Maximum frame average light level (source)
MaxFALL_Original          : Maximum frame average light level (if incoherencies)
MaxFALL_Original_Source   : Maximum frame average light level (source if incoherencies)
 
Audio 
Count                     : Count of objects available in this stream
Status                    : bit field (0=IsAccepted, 1=IsFilled, 2=IsUpdated, 3=IsFinished)
StreamCount               : Count of streams of that kind available
StreamKind                : Stream type name
StreamKind/String         : Stream type name
StreamKindID              : Number of the stream (base=0)
StreamKindPos             : When multiple streams, number of the stream (base=1)
StreamOrder               : Stream order in the file, whatever is the kind of stream (base=0)
FirstPacketOrder          : Order of the first fully decodable packet met in the file, whatever is the kind of stream (base=0)
Inform                    : Last **Inform** call
ID                        : The ID for this stream in this file
ID/String                 : The ID for this stream in this file
OriginalSourceMedium_ID   : The ID for this stream in the original medium of the material
OriginalSourceMedium_ID/S : The ID for this stream in the original medium of the material
UniqueID                  : The unique ID for this stream, should be copied with stream copy
UniqueID/String           : The unique ID for this stream, should be copied with stream copy
MenuID                    : The menu ID for this stream in this file
MenuID/String             : The menu ID for this stream in this file
Format                    : Format used
Format/String             : Format used + additional features
Format/Info               : Info about the format
Format/Url                : Homepage of this format
Format_Commercial         : Commercial name used by vendor for theses setings or Format field if there is no difference
Format_Commercial_IfAny   : Commercial name used by vendor for theses setings if there is one
Format_Version            : Version of this format
Format_Profile            : Profile of the Format (old XML: 'Profile@Level' format
Format_Level              : Level of the Format (only MIXML)
Format_Compression        : Compression method used
Format_Settings           : Settings needed for decoder used, summary
Format_Settings_SBR 
Format_Settings_SBR/String 
Format_Settings_PS 
Format_Settings_PS/String 
Format_Settings_Mode 
Format_Settings_ModeExtension 
Format_Settings_Emphasis 
Format_Settings_Floor 
Format_Settings_Firm 
Format_Settings_Endianness 
Format_Settings_Sign 
Format_Settings_Law 
Format_Settings_ITU 
Format_Settings_Wrapping  : Wrapping mode (Frame wrapped or Clip wrapped)
Format_AdditionalFeatures : Format features needed for fully supporting the content
Matrix_Format             : Matrix format (e.g. DTS Neural)
InternetMediaType         : Internet Media Type (aka MIME Type, Content-Type)
MuxingMode                : How this stream is muxed in the container
MuxingMode_MoreInfo       : More info (text) about the muxing mode
CodecID                   : Codec ID (found in some containers)
CodecID/String            : Codec ID (found in some containers)
CodecID/Info              : Info about codec ID
CodecID/Hint              : Hint/popular name for this codec ID
CodecID/Url               : Homepage for more details about this codec ID
CodecID_Description       : Manual description given by the container
Codec                     : Deprecated, do not use in new projects
Codec/String              : Deprecated, do not use in new projects
Codec/Family              : Deprecated, do not use in new projects
Codec/Info                : Deprecated, do not use in new projects
Codec/Url                 : Deprecated, do not use in new projects
Codec/CC                  : Deprecated, do not use in new projects
Codec_Description         : Deprecated, do not use in new projects
Codec_Profile             : Deprecated, do not use in new projects
Codec_Settings            : Deprecated, do not use in new projects
Codec_Settings_Automatic  : Deprecated, do not use in new projects
Codec_Settings_Floor      : Deprecated, do not use in new projects
Codec_Settings_Firm       : Deprecated, do not use in new projects
Codec_Settings_Endianness : Deprecated, do not use in new projects
Codec_Settings_Sign       : Deprecated, do not use in new projects
Codec_Settings_Law        : Deprecated, do not use in new projects
Codec_Settings_ITU        : Deprecated, do not use in new projects
Duration                  : Play time of the stream, in ms
Duration/String           : Play time in format : XXx YYy only, YYy omited if zero
Duration/String1          : Play time in format : HHh MMmn SSs MMMms, XX omited if zero
Duration/String2          : Play time in format : XXx YYy only, YYy omited if zero
Duration/String3          : Play time in format : HH:MM:SS.MMM
Duration/String4          : Play time in format : HH:MM:SS:FF, last colon replaced by semicolon for drop frame if available
Duration/String5          : Play time in format : HH:MM:SS.mmm (HH:MM:SS:FF)
Duration_FirstFrame       : Duration of the first frame if it is longer than others, in ms
Duration_FirstFrame/Strin : Duration of the first frame if it is longer than others, in format : XXx YYy only, YYy omited if zero
Duration_FirstFrame/Strin : Duration of the first frame if it is longer than others, in format : HHh MMmn SSs MMMms, XX omited if zero
Duration_FirstFrame/Strin : Duration of the first frame if it is longer than others, in format : XXx YYy only, YYy omited if zero
Duration_FirstFrame/Strin : Duration of the first frame if it is longer than others, in format : HH:MM:SS.MMM
Duration_FirstFrame/Strin : Play time in format : HH:MM:SS:FF, last colon replaced by semicolon for drop frame if available
Duration_FirstFrame/Strin : Play time in format : HH:MM:SS.mmm (HH:MM:SS:FF)
Duration_LastFrame        : Duration of the last frame if it is longer than others, in ms
Duration_LastFrame/String : Duration of the last frame if it is longer than others, in format : XXx YYy only, YYy omited if zero
Duration_LastFrame/String : Duration of the last frame if it is longer than others, in format : HHh MMmn SSs MMMms, XX omited if zero
Duration_LastFrame/String : Duration of the last frame if it is longer than others, in format : XXx YYy only, YYy omited if zero
Duration_LastFrame/String : Duration of the last frame if it is longer than others, in format : HH:MM:SS.MMM
Duration_LastFrame/String : Play time in format : HH:MM:SS:FF, last colon replaced by semicolon for drop frame if available
Duration_LastFrame/String : Play time in format : HH:MM:SS.mmm (HH:MM:SS:FF)
Source_Duration           : Source Play time of the stream, in ms
Source_Duration/String    : Source Play time in format : XXx YYy only, YYy omited if zero
Source_Duration/String1   : Source Play time in format : HHh MMmn SSs MMMms, XX omited if zero
Source_Duration/String2   : Source Play time in format : XXx YYy only, YYy omited if zero
Source_Duration/String3   : Source Play time in format : HH:MM:SS.MMM
Source_Duration/String4   : Source Play time in format : HH:MM:SS:FF, last colon replaced by semicolon for drop frame if available
Source_Duration/String5   : Source Play time in format : HH:MM:SS.mmm (HH:MM:SS:FF)
Source_Duration_FirstFram : Source Duration of the first frame if it is longer than others, in ms
Source_Duration_FirstFram : Source Duration of the first frame if it is longer than others, in format : XXx YYy only, YYy omited if zero
Source_Duration_FirstFram : Source Duration of the first frame if it is longer than others, in format : HHh MMmn SSs MMMms, XX omited if zero
Source_Duration_FirstFram : Source Duration of the first frame if it is longer than others, in format : XXx YYy only, YYy omited if zero
Source_Duration_FirstFram : Source Duration of the first frame if it is longer than others, in format : HH:MM:SS.MMM
Source_Duration_FirstFram : Source Duration of the first frame if it is longer than others, in format : HH:MM:SS:FF, last colon replaced by semicolon for drop frame if available
Source_Duration_FirstFram : Source Duration of the first frame if it is longer than others, in format : HH:MM:SS.mmm (HH:MM:SS:FF)
Source_Duration_LastFrame : Source Duration of the last frame if it is longer than others, in ms
Source_Duration_LastFrame : Source Duration of the last frame if it is longer than others, in format : XXx YYy only, YYy omited if zero
Source_Duration_LastFrame : Source Duration of the last frame if it is longer than others, in format : HHh MMmn SSs MMMms, XX omited if zero
Source_Duration_LastFrame : Source Duration of the last frame if it is longer than others, in format : XXx YYy only, YYy omited if zero
Source_Duration_LastFrame : Source Duration of the last frame if it is longer than others, in format : HH:MM:SS.MMM
Source_Duration_LastFrame : Source Duration of the last frame if it is longer than others, in format : HH:MM:SS:FF, last colon replaced by semicolon for drop frame if available
Source_Duration_LastFrame : Source Duration of the last frame if it is longer than others, in format : HH:MM:SS.mmm (HH:MM:SS:FF)
BitRate_Mode              : Bit rate mode (VBR, CBR)
BitRate_Mode/String       : Bit rate mode (Constant, Variable)
BitRate                   : Bit rate in bps
BitRate/String            : Bit rate (with measurement)
BitRate_Minimum           : Minimum Bit rate in bps
BitRate_Minimum/String    : Minimum Bit rate (with measurement)
BitRate_Nominal           : Nominal Bit rate in bps
BitRate_Nominal/String    : Nominal Bit rate (with measurement)
BitRate_Maximum           : Maximum Bit rate in bps
BitRate_Maximum/String    : Maximum Bit rate (with measurement)
BitRate_Encoded           : Encoded (with forced padding) bit rate in bps, if some container padding is present
BitRate_Encoded/String    : Encoded (with forced padding) bit rate (with measurement), if some container padding is present
Channel(s)                : Number of channels
Channel(s)/String         : Number of channels (with measurement)
Channel(s)_Original       : Number of channels
Channel(s)_Original/Strin : Number of channels (with measurement)
Matrix_Channel(s)         : Number of channels after matrix decoding
Matrix_Channel(s)/String  : Number of channels after matrix decoding (with measurement)
ChannelPositions          : Position of channels
ChannelPositions_Original : Position of channels
ChannelPositions/String2  : Position of channels (x/y.z format)
ChannelPositions_Original : Position of channels (x/y.z format)
Matrix_ChannelPositions   : Position of channels after matrix decoding
Matrix_ChannelPositions/S : Position of channels after matrix decoding (x/y.z format)
ChannelLayout             : Layout of channels (in the stream)
ChannelLayout_Original    : Layout of channels (in the stream)
ChannelLayoutID           : ID of layout of channels (e.g. MXF descriptor channel assignment). Warning, sometimes this is not enough for uniquely identifying a layout (e.g. MXF descriptor channel assignment is SMPTE 377-4). For AC-3, the form is x,y with x=acmod and y=lfeon.
SamplesPerFrame           : Sampling rate
SamplingRate              : Sampling rate
SamplingRate/String       : in KHz
SamplingCount             : Sample count (based on sampling rate)
Source_SamplingCount      : Source Sample count (based on sampling rate)
FrameRate                 : Frames per second
FrameRate/String          : Frames per second (with measurement)
FrameRate_Num             : Frames per second, numerator
FrameRate_Den             : Frames per second, denominator
FrameCount                : Frame count (a frame contains a count of samples depends of the format)
Source_FrameCount         : Source Frame count (a frame contains a count of samples depends of the format)
Resolution                : Deprecated, do not use in new projects
Resolution/String         : Deprecated, do not use in new projects
BitDepth                  : Resolution in bits (8, 16, 20, 24). Note: significant bits in case the stored bit depth is different
BitDepth/String           : Resolution in bits (8, 16, 20, 24). Note: significant bits in case the stored bit depth is different
BitDepth_Detected         : Detected (during scan of the input by the muxer) resolution in bits
BitDepth_Detected/String  : Detected (during scan of the input by the muxer) resolution in bits
BitDepth_Stored           : Stored Resolution in bits (8, 16, 20, 24)
BitDepth_Stored/String    : Stored Resolution in bits (8, 16, 20, 24)
Compression_Mode          : Compression mode (Lossy or Lossless)
Compression_Mode/String   : Compression mode (Lossy or Lossless)
Compression_Ratio         : Current stream size divided by uncompressed stream size
Delay                     : Delay fixed in the stream (relative) IN MS
Delay/String              : Delay with measurement
Delay/String1             : Delay with measurement
Delay/String2             : Delay with measurement
Delay/String3             : Delay in format : HH:MM:SS.MMM
Delay/String4             : Delay in format : HH:MM:SS:FF, last colon replaced by semicolon for drop frame if available
Delay/String5             : Delay in format : HH:MM:SS.mmm (HH:MM:SS:FF)
Delay_Settings            : Delay settings (in case of timecode for example)
Delay_DropFrame           : Delay drop frame
Delay_Source              : Delay source (Container or Stream or empty)
Delay_Source/String       : Delay source (Container or Stream or empty)
Delay_Original            : Delay fixed in the raw stream (relative) IN MS
Delay_Original/String     : Delay with measurement
Delay_Original/String1    : Delay with measurement
Delay_Original/String2    : Delay with measurement
Delay_Original/String3    : Delay in format: HH:MM:SS.MMM
Delay_Original/String4    : Delay in format : HH:MM:SS:FF, last colon replaced by semicolon for drop frame if available
Delay_Original/String5    : Delay in format : HH:MM:SS.mmm (HH:MM:SS:FF)
Delay_Original_Settings   : Delay settings (in case of timecode for example)
Delay_Original_DropFrame  : Delay drop frame info
Delay_Original_Source     : Delay source (Stream or empty)
Video_Delay               : Delay fixed in the stream (absolute / video)
Video_Delay/String 
Video_Delay/String1 
Video_Delay/String2 
Video_Delay/String3 
Video_Delay/String4 
Video_Delay/String5 
Video0_Delay              : Deprecated, do not use in new projects
Video0_Delay/String       : Deprecated, do not use in new projects
Video0_Delay/String1      : Deprecated, do not use in new projects
Video0_Delay/String2      : Deprecated, do not use in new projects
Video0_Delay/String3      : Deprecated, do not use in new projects
Video0_Delay/String4      : Deprecated, do not use in new projects
Video0_Delay/String5      : Deprecated, do not use in new projects
ReplayGain_Gain           : The gain to apply to reach 89dB SPL on playback
ReplayGain_Gain/String 
ReplayGain_Peak           : The maximum absolute peak value of the item
StreamSize                : Streamsize in bytes
StreamSize/String         : Streamsize in with percentage value
StreamSize/String1 
StreamSize/String2 
StreamSize/String3 
StreamSize/String4 
StreamSize/String5        : Streamsize in with percentage value
StreamSize_Proportion     : Stream size divided by file size
StreamSize_Demuxed        : StreamSize in bytes of hte stream after demux
StreamSize_Demuxed/String : StreamSize_Demuxed in with percentage value
StreamSize_Demuxed/String1 
StreamSize_Demuxed/String2 
StreamSize_Demuxed/String3 
StreamSize_Demuxed/String4 
StreamSize_Demuxed/String : StreamSize_Demuxed in with percentage value (note: theoritical value, not for real use)
Source_StreamSize         : Source Streamsize in bytes
Source_StreamSize/String  : Source Streamsize in with percentage value
Source_StreamSize/String1 
Source_StreamSize/String2 
Source_StreamSize/String3 
Source_StreamSize/String4 
Source_StreamSize/String5 : Source Streamsize in with percentage value
Source_StreamSize_Proport : Source Stream size divided by file size
StreamSize_Encoded        : Encoded Streamsize in bytes
StreamSize_Encoded/String : Encoded Streamsize in with percentage value
StreamSize_Encoded/String1 
StreamSize_Encoded/String2 
StreamSize_Encoded/String3 
StreamSize_Encoded/String4 
StreamSize_Encoded/String : Encoded Streamsize in with percentage value
StreamSize_Encoded_Propor : Encoded Stream size divided by file size
Source_StreamSize_Encoded : Source Encoded Streamsize in bytes
Source_StreamSize_Encoded : Source Encoded Streamsize in with percentage value
Source_StreamSize_Encoded/String1 
Source_StreamSize_Encoded/String2 
Source_StreamSize_Encoded/String3 
Source_StreamSize_Encoded/String4 
Source_StreamSize_Encoded : Source Encoded Streamsize in with percentage value
Source_StreamSize_Encoded : Source Encoded Stream size divided by file size
Alignment                 : How this stream file is aligned in the container
Alignment/String          : Where this stream file is aligned in the container
Interleave_VideoFrames    : Between how many video frames the stream is inserted
Interleave_Duration       : Between how much time (ms) the stream is inserted
Interleave_Duration/Strin : Between how much time and video frames the stream is inserted (with measurement)
Interleave_Preload        : How much time is buffered before the first video frame
Interleave_Preload/String : How much time is buffered before the first video frame (with measurement)
Title                     : Name of the track
Encoded_Application       : Name of the software package used to create the file, such as Microsoft WaveEdit
Encoded_Application/Strin : Name of the software package used to create the file, such as Microsoft WaveEdit, trying to have the format 'CompanyName ProductName (OperatingSystem) Version (Date)'
Encoded_Application_Compa : Name of the company
Encoded_Application_Name  : Name of the product
Encoded_Application_Versi : Version of the product
Encoded_Application_Url   : Name of the software package used to create the file, such as Microsoft WaveEdit.
Encoded_Library           : Software used to create the file
Encoded_Library/String    : Software used to create the file, trying to have the format 'CompanyName ProductName (OperatingSystem) Version (Date)'
Encoded_Library_CompanyNa : Name of the company
Encoded_Library_Name      : Name of the the encoding-software
Encoded_Library_Version   : Version of encoding-software
Encoded_Library_Date      : Release date of software
Encoded_Library_Settings  : Parameters used by the software
Encoded_OperatingSystem   : Operating System of encoding-software
Language                  : Language (2-letter ISO 639-1 if exists, else 3-letter ISO 639-2, and with optional ISO 3166-1 country separated by a dash if available, e.g. en, en-us, zh-cn)
Language/String           : Language (full)
Language/String1          : Language (full)
Language/String2          : Language (2-letter ISO 639-1 if exists, else empty)
Language/String3          : Language (3-letter ISO 639-2 if exists, else empty)
Language/String4          : Language (2-letter ISO 639-1 if exists with optional ISO 3166-1 country separated by a dash if available, e.g. en, en-us, zh-cn, else empty)
Language_More             : More info about Language (e.g. Director's Comment)
ServiceKind               : Service kind, e.g. visually impaired, commentary, voice over
ServiceKind/String        : Service kind (full)
Disabled                  : Set if that track should not be used
Disabled/String           : Set if that track should not be used
Default                   : Set if that track should be used if no language found matches the user preference.
Default/String            : Set if that track should be used if no language found matches the user preference.
Forced                    : Set if that track should be used if no language found matches the user preference.
Forced/String             : Set if that track should be used if no language found matches the user preference.
AlternateGroup            : Number of a group in order to provide versions of the same track
AlternateGroup/String     : Number of a group in order to provide versions of the same track
Encoded_Date              : UTC time that the encoding of this item was completed began.
Tagged_Date               : UTC time that the tags were done for this item.
Encryption 
 
Text 
Count                     : Count of objects available in this stream
Status                    : bit field (0=IsAccepted, 1=IsFilled, 2=IsUpdated, 3=IsFinished)
StreamCount               : Count of streams of that kind available
StreamKind                : Stream type name
StreamKind/String         : Stream type name
StreamKindID              : Number of the stream (base=0)
StreamKindPos             : When multiple streams, number of the stream (base=1)
StreamOrder               : Stream order in the file, whatever is the kind of stream (base=0)
FirstPacketOrder          : Order of the first fully decodable packet met in the file, whatever is the kind of stream (base=0)
Inform                    : Last **Inform** call
ID                        : The ID for this stream in this file
ID/String                 : The ID for this stream in this file
OriginalSourceMedium_ID   : The ID for this stream in the original medium of the material
OriginalSourceMedium_ID/S : The ID for this stream in the original medium of the material
UniqueID                  : The unique ID for this stream, should be copied with stream copy
UniqueID/String           : The unique ID for this stream, should be copied with stream copy
MenuID                    : The menu ID for this stream in this file
MenuID/String             : The menu ID for this stream in this file
Format                    : Format used
Format/String             : Format used + additional features
Format/Info               : Info about Format
Format/Url                : Link
Format_Commercial         : Commercial name used by vendor for theses setings or Format field if there is no difference
Format_Commercial_IfAny   : Commercial name used by vendor for theses setings if there is one
Format_Version            : Version of this format
Format_Profile            : Profile of the Format
Format_Compression        : Compression method used
Format_Settings           : Settings needed for decoder used
Format_Settings_Wrapping  : Wrapping mode (Frame wrapped or Clip wrapped)
Format_AdditionalFeatures : Format features needed for fully supporting the content
InternetMediaType         : Internet Media Type (aka MIME Type, Content-Type)
MuxingMode                : How this stream is muxed in the container
MuxingMode_MoreInfo       : More info (text) about the muxing mode
CodecID                   : Codec ID (found in some containers)
CodecID/String            : Codec ID (found in some containers)
CodecID/Info              : Info about codec ID
CodecID/Hint              : A hint for this codec ID
CodecID/Url               : A link for more details about this codec ID
CodecID_Description       : Manual description given by the container
Codec                     : Deprecated
Codec/String              : Deprecated
Codec/Info                : Deprecated
Codec/Url                 : Deprecated
Codec/CC                  : Deprecated
Duration                  : Play time of the stream, in ms
Duration/String           : Play time (formated)
Duration/String1          : Play time in format : HHh MMmn SSs MMMms, XX omited if zero
Duration/String2          : Play time in format : XXx YYy only, YYy omited if zero
Duration/String3          : Play time in format : HH:MM:SS.MMM
Duration/String4          : Play time in format : HH:MM:SS:FF, last colon replaced by semicolon for drop frame if available
Duration/String5          : Play time in format : HH:MM:SS.mmm (HH:MM:SS:FF)
Duration_FirstFrame       : Duration of the first frame if it is longer than others, in ms
Duration_FirstFrame/Strin : Duration of the first frame if it is longer than others, in format : XXx YYy only, YYy omited if zero
Duration_FirstFrame/Strin : Duration of the first frame if it is longer than others, in format : HHh MMmn SSs MMMms, XX omited if zero
Duration_FirstFrame/Strin : Duration of the first frame if it is longer than others, in format : XXx YYy only, YYy omited if zero
Duration_FirstFrame/Strin : Duration of the first frame if it is longer than others, in format : HH:MM:SS.MMM
Duration_FirstFrame/Strin : Duration of the first frame if it is longer than others, in format : HH:MM:SS:FF, last colon replaced by semicolon for drop frame if available
Duration_FirstFrame/Strin : Duration of the first frame if it is longer than others, in format : HH:MM:SS.mmm (HH:MM:SS:FF)
Duration_LastFrame        : Duration of the last frame if it is longer than others, in ms
Duration_LastFrame/String : Duration of the last frame if it is longer than others, in format : XXx YYy only, YYy omited if zero
Duration_LastFrame/String : Duration of the last frame if it is longer than others, in format : HHh MMmn SSs MMMms, XX omited if zero
Duration_LastFrame/String : Duration of the last frame if it is longer than others, in format : XXx YYy only, YYy omited if zero
Duration_LastFrame/String : Duration of the last frame if it is longer than others, in format : HH:MM:SS.MMM
Duration_LastFrame/String : Duration of the last frame if it is longer than others, in format : HH:MM:SS:FF, last colon replaced by semicolon for drop frame if available
Duration_LastFrame/String : Duration of the last frame if it is longer than others, in format : HH:MM:SS.mmm (HH:MM:SS:FF)
Source_Duration           : Source Play time of the stream, in ms
Source_Duration/String    : Source Play time in format : XXx YYy only, YYy omited if zero
Source_Duration/String1   : Source Play time in format : HHh MMmn SSs MMMms, XX omited if zero
Source_Duration/String2   : Source Play time in format : XXx YYy only, YYy omited if zero
Source_Duration/String3   : Source Play time in format : HH:MM:SS.MMM
Source_Duration/String4   : Source Play time in format : HH:MM:SS:FF, last colon replaced by semicolon for drop frame if available
Source_Duration/String5   : Source Play time in format : HH:MM:SS.mmm (HH:MM:SS:FF)
Source_Duration_FirstFram : Source Duration of the first frame if it is longer than others, in ms
Source_Duration_FirstFram : Source Duration of the first frame if it is longer than others, in format : XXx YYy only, YYy omited if zero
Source_Duration_FirstFram : Source Duration of the first frame if it is longer than others, in format : HHh MMmn SSs MMMms, XX omited if zero
Source_Duration_FirstFram : Source Duration of the first frame if it is longer than others, in format : XXx YYy only, YYy omited if zero
Source_Duration_FirstFram : Source Duration of the first frame if it is longer than others, in format : HH:MM:SS.MMM
Source_Duration_FirstFram : Source Duration of the first frame if it is longer than others, in format : HH:MM:SS:FF, last colon replaced by semicolon for drop frame if available
Source_Duration_FirstFram : Source Duration of the first frame if it is longer than others, in format : HH:MM:SS.mmm (HH:MM:SS:FF)
Source_Duration_LastFrame : Source Duration of the last frame if it is longer than others, in ms
Source_Duration_LastFrame : Source Duration of the last frame if it is longer than others, in format : XXx YYy only, YYy omited if zero
Source_Duration_LastFrame : Source Duration of the last frame if it is longer than others, in format : HHh MMmn SSs MMMms, XX omited if zero
Source_Duration_LastFrame : Source Duration of the last frame if it is longer than others, in format : XXx YYy only, YYy omited if zero
Source_Duration_LastFrame : Source Duration of the last frame if it is longer than others, in format : HH:MM:SS.MMM
Source_Duration_LastFrame : Source Duration of the last frame if it is longer than others, in format : HH:MM:SS:FF, last colon replaced by semicolon for drop frame if available
Source_Duration_LastFrame : Source Duration of the last frame if it is longer than others, in format : HH:MM:SS.mmm (HH:MM:SS:FF)
BitRate_Mode              : Bit rate mode (VBR, CBR)
BitRate_Mode/String       : Bit rate mode (Constant, Variable)
BitRate                   : Bit rate in bps
BitRate/String            : Bit rate (with measurement)
BitRate_Minimum           : Minimum Bit rate in bps
BitRate_Minimum/String    : Minimum Bit rate (with measurement)
BitRate_Nominal           : Nominal Bit rate in bps
BitRate_Nominal/String    : Nominal Bit rate (with measurement)
BitRate_Maximum           : Maximum Bit rate in bps
BitRate_Maximum/String    : Maximum Bit rate (with measurement)
BitRate_Encoded           : Encoded (with forced padding) bit rate in bps, if some container padding is present
BitRate_Encoded/String    : Encoded (with forced padding) bit rate (with measurement), if some container padding is present
Width                     : Width
Width/String 
Height                    : Height
Height/String 
FrameRate_Mode            : Frame rate mode (CFR, VFR)
FrameRate_Mode/String     : Frame rate mode (Constant, Variable)
FrameRate                 : Frames per second
FrameRate/String          : Frames per second (with measurement)
FrameRate_Num             : Frames per second, numerator
FrameRate_Den             : Frames per second, denominator
FrameRate_Minimum         : Minimum Frames per second
FrameRate_Minimum/String  : Minimum Frames per second (with measurement)
FrameRate_Nominal         : Nominal Frames per second
FrameRate_Nominal/String  : Nominal Frames per second (with measurement)
FrameRate_Maximum         : Maximum Frames per second
FrameRate_Maximum/String  : Maximum Frames per second (with measurement)
FrameRate_Original        : Original (in the raw stream) Frames per second
FrameRate_Original/String : Original (in the raw stream) Frames per second (with measurement)
FrameCount                : Number of frames
ElementCount              : Number of displayed elements
Source_FrameCount         : Source Number of frames
ColorSpace 
ChromaSubsampling 
Resolution                : Deprecated, do not use in new projects
Resolution/String         : Deprecated, do not use in new projects
BitDepth 
BitDepth/String 
Compression_Mode          : Compression mode (Lossy or Lossless)
Compression_Mode/String   : Compression mode (Lossy or Lossless)
Compression_Ratio         : Current stream size divided by uncompressed stream size
Delay                     : Delay fixed in the stream (relative) IN MS
Delay/String              : Delay with measurement
Delay/String1             : Delay with measurement
Delay/String2             : Delay with measurement
Delay/String3             : Delay in format : HH:MM:SS.MMM
Delay/String4             : Delay in format : HH:MM:SS:FF, last colon replaced by semicolon for drop frame if available
Delay/String5             : Delay in format : HH:MM:SS.mmm (HH:MM:SS:FF)
Delay_Settings            : Delay settings (in case of timecode for example)
Delay_DropFrame           : Delay drop frame
Delay_Source              : Delay source (Container or Stream or empty)
Delay_Source/String       : Delay source (Container or Stream or empty)
Delay_Original            : Delay fixed in the raw stream (relative) IN MS
Delay_Original/String     : Delay with measurement
Delay_Original/String1    : Delay with measurement
Delay_Original/String2    : Delay with measurement
Delay_Original/String3    : Delay in format: HH:MM:SS.MMM
Delay_Original/String4    : Delay in format: HH:MM:SS:FF, last colon replaced by semicolon for drop frame if available
Delay_Original/String5    : Delay in format : HH:MM:SS.mmm (HH:MM:SS:FF)
Delay_Original_Settings   : Delay settings (in case of timecode for example)
Delay_Original_DropFrame  : Delay drop frame info
Delay_Original_Source     : Delay source (Stream or empty)
Video_Delay               : Delay fixed in the stream (absolute / video)
Video_Delay/String 
Video_Delay/String1 
Video_Delay/String2 
Video_Delay/String3 
Video_Delay/String4 
Video_Delay/String5 
Video0_Delay              : Deprecated, do not use in new projects
Video0_Delay/String       : Deprecated, do not use in new projects
Video0_Delay/String1      : Deprecated, do not use in new projects
Video0_Delay/String2      : Deprecated, do not use in new projects
Video0_Delay/String3      : Deprecated, do not use in new projects
Video0_Delay/String4      : Deprecated, do not use in new projects
Video0_Delay/String5      : Deprecated, do not use in new projects
StreamSize                : Streamsize in bytes
StreamSize/String         : Streamsize in with percentage value
StreamSize/String1 
StreamSize/String2 
StreamSize/String3 
StreamSize/String4 
StreamSize/String5        : Streamsize in with percentage value
StreamSize_Proportion     : Stream size divided by file size
StreamSize_Demuxed        : StreamSize in bytes of hte stream after demux
StreamSize_Demuxed/String : StreamSize_Demuxed in with percentage value
StreamSize_Demuxed/String1 
StreamSize_Demuxed/String2 
StreamSize_Demuxed/String3 
StreamSize_Demuxed/String4 
StreamSize_Demuxed/String : StreamSize_Demuxed in with percentage value (note: theoritical value, not for real use)
Source_StreamSize         : Source Streamsize in bytes
Source_StreamSize/String  : Source Streamsize in with percentage value
Source_StreamSize/String1 
Source_StreamSize/String2 
Source_StreamSize/String3 
Source_StreamSize/String4 
Source_StreamSize/String5 : Source Streamsize in with percentage value
Source_StreamSize_Proport : Source Stream size divided by file size
StreamSize_Encoded        : Encoded Streamsize in bytes
StreamSize_Encoded/String : Encoded Streamsize in with percentage value
StreamSize_Encoded/String1 
StreamSize_Encoded/String2 
StreamSize_Encoded/String3 
StreamSize_Encoded/String4 
StreamSize_Encoded/String : Encoded Streamsize in with percentage value
StreamSize_Encoded_Propor : Encoded Stream size divided by file size
Source_StreamSize_Encoded : Source Encoded Streamsize in bytes
Source_StreamSize_Encoded : Source Encoded Streamsize in with percentage value
Source_StreamSize_Encoded/String1 
Source_StreamSize_Encoded/String2 
Source_StreamSize_Encoded/String3 
Source_StreamSize_Encoded/String4 
Source_StreamSize_Encoded : Source Encoded Streamsize in with percentage value
Source_StreamSize_Encoded : Source Encoded Stream size divided by file size
Title                     : Name of the track
Encoded_Application       : Name of the software package used to create the file, such as Microsoft WaveEdit
Encoded_Application/Strin : Name of the software package used to create the file, such as Microsoft WaveEdit, trying to have the format 'CompanyName ProductName (OperatingSystem) Version (Date)'
Encoded_Application_Compa : Name of the company
Encoded_Application_Name  : Name of the product
Encoded_Application_Versi : Version of the product
Encoded_Application_Url   : Name of the software package used to create the file, such as Microsoft WaveEdit.
Encoded_Library           : Software used to create the file
Encoded_Library/String    : Software used to create the file, trying to have the format 'CompanyName ProductName (OperatingSystem) Version (Date)'
Encoded_Library_CompanyNa : Name of the company
Encoded_Library_Name      : Name of the the encoding-software
Encoded_Library_Version   : Version of encoding-software
Encoded_Library_Date      : Release date of software
Encoded_Library_Settings  : Parameters used by the software
Encoded_OperatingSystem   : Operating System of encoding-software
Language                  : Language (2-letter ISO 639-1 if exists, else 3-letter ISO 639-2, and with optional ISO 3166-1 country separated by a dash if available, e.g. en, en-us, zh-cn)
Language/String           : Language (full)
Language/String1          : Language (full)
Language/String2          : Language (2-letter ISO 639-1 if exists, else empty)
Language/String3          : Language (3-letter ISO 639-2 if exists, else empty)
Language/String4          : Language (2-letter ISO 639-1 if exists with optional ISO 3166-1 country separated by a dash if available, e.g. en, en-us, zh-cn, else empty)
Language_More             : More info about Language (e.g. Director's Comment)
ServiceKind               : Service kind, e.g. visually impaired, commentary, voice over
ServiceKind/String        : Service kind (full)
Disabled                  : Set if that track should not be used
Disabled/String           : Set if that track should not be used
Default                   : Set if that track should be used if no language found matches the user preference.
Default/String            : Set if that track should be used if no language found matches the user preference.
Forced                    : Set if that track should be used if no language found matches the user preference.
Forced/String             : Set if that track should be used if no language found matches the user preference.
AlternateGroup            : Number of a group in order to provide versions of the same track
AlternateGroup/String     : Number of a group in order to provide versions of the same track
Summary 
Encoded_Date              : The time that the encoding of this item was completed began.
Tagged_Date               : The time that the tags were done for this item.
Encryption 
 
Other 
Count                     : Count of objects available in this stream
Status                    : bit field (0=IsAccepted, 1=IsFilled, 2=IsUpdated, 3=IsFinished)
StreamCount               : Count of streams of that kind available
StreamKind                : Stream type name
StreamKind/String         : Stream type name
StreamKindID              : Number of the stream (base=0)
StreamKindPos             : When multiple streams, number of the stream (base=1)
StreamOrder               : Stream order in the file, whatever is the kind of stream (base=0)
FirstPacketOrder          : Order of the first fully decodable packet met in the file, whatever is the kind of stream (base=0)
Inform                    : Last **Inform** call
ID                        : The ID for this stream in this file
ID/String                 : The ID for this stream in this file
OriginalSourceMedium_ID   : The ID for this stream in the original medium of the material
OriginalSourceMedium_ID/S : The ID for this stream in the original medium of the material
UniqueID                  : The unique ID for this stream, should be copied with stream copy
UniqueID/String           : The unique ID for this stream, should be copied with stream copy
MenuID                    : The menu ID for this stream in this file
MenuID/String             : The menu ID for this stream in this file
Type                      : Type
Format                    : Format used
Format/String             : Format used + additional features
Format/Info               : Info about Format
Format/Url                : Link
Format_Commercial         : Commercial name used by vendor for theses setings or Format field if there is no difference
Format_Commercial_IfAny   : Commercial name used by vendor for theses setings if there is one
Format_Version            : Version of this format
Format_Profile            : Profile of the Format
Format_Compression        : Compression method used
Format_Settings           : Settings needed for decoder used
Format_AdditionalFeatures : Format features needed for fully supporting the content
MuxingMode                : How this file is muxed in the container
CodecID                   : Codec ID (found in some containers)
CodecID/String            : Codec ID (found in some containers)
CodecID/Info              : Info about this codec
CodecID/Hint              : A hint/popular name for this codec
CodecID/Url               : A link to more details about this codec ID
CodecID_Description       : Manual description given by the container
Duration                  : Play time of the stream in ms
Duration/String           : Play time in format : XXx YYy only, YYy omited if zero
Duration/String1          : Play time in format : HHh MMmn SSs MMMms, XX omited if zero
Duration/String2          : Play time in format : XXx YYy only, YYy omited if zero
Duration/String3          : Play time in format : HH:MM:SS.MMM
Duration/String4          : Play time in format : HH:MM:SS:FF, last colon replaced by semicolon for drop frame if available
Duration/String5          : Play time in format : HH:MM:SS.mmm (HH:MM:SS:FF)
Duration_Start 
Duration_End 
Source_Duration           : Source Play time of the stream, in ms
Source_Duration/String    : Source Play time in format : XXx YYy only, YYy omited if zero
Source_Duration/String1   : Source Play time in format : HHh MMmn SSs MMMms, XX omited if zero
Source_Duration/String2   : Source Play time in format : XXx YYy only, YYy omited if zero
Source_Duration/String3   : Source Play time in format : HH:MM:SS.MMM
Source_Duration/String4   : Play time in format : HH:MM:SS:FF, last colon replaced by semicolon for drop frame if available
Source_Duration/String5   : Play time in format : HH:MM:SS.mmm (HH:MM:SS:FF)
Source_Duration_FirstFram : Source Duration of the first frame if it is longer than others, in ms
Source_Duration_FirstFram : Source Duration of the first frame if it is longer than others, in format : XXx YYy only, YYy omited if zero
Source_Duration_FirstFram : Source Duration of the first frame if it is longer than others, in format : HHh MMmn SSs MMMms, XX omited if zero
Source_Duration_FirstFram : Source Duration of the first frame if it is longer than others, in format : XXx YYy only, YYy omited if zero
Source_Duration_FirstFram : Source Duration of the first frame if it is longer than others, in format : HH:MM:SS.MMM
Source_Duration_FirstFram : Play time in format : HH:MM:SS:FF, last colon replaced by semicolon for drop frame if available
Source_Duration_FirstFram : Play time in format : HH:MM:SS.mmm (HH:MM:SS:FF)
Source_Duration_LastFrame : Source Duration of the last frame if it is longer than others, in ms
Source_Duration_LastFrame : Source Duration of the last frame if it is longer than others, in format : XXx YYy only, YYy omited if zero
Source_Duration_LastFrame : Source Duration of the last frame if it is longer than others, in format : HHh MMmn SSs MMMms, XX omited if zero
Source_Duration_LastFrame : Source Duration of the last frame if it is longer than others, in format : XXx YYy only, YYy omited if zero
Source_Duration_LastFrame : Source Duration of the last frame if it is longer than others, in format : HH:MM:SS.MMM
Source_Duration_LastFrame : Play time in format : HH:MM:SS:FF, last colon replaced by semicolon for drop frame if available
Source_Duration_LastFrame : Play time in format : HH:MM:SS.mmm (HH:MM:SS:FF)
BitRate_Mode              : Bit rate mode (VBR, CBR)
BitRate_Mode/String       : Bit rate mode (Variable, Cconstant)
BitRate                   : Bit rate in bps
BitRate/String            : Bit rate (with measurement)
BitRate_Minimum           : Minimum Bit rate in bps
BitRate_Minimum/String    : Minimum Bit rate (with measurement)
BitRate_Nominal           : Nominal Bit rate in bps
BitRate_Nominal/String    : Nominal Bit rate (with measurement)
BitRate_Maximum           : Maximum Bit rate in bps
BitRate_Maximum/String    : Maximum Bit rate (with measurement)
BitRate_Encoded           : Encoded (with forced padding) bit rate in bps, if some container padding is present
BitRate_Encoded/String    : Encoded (with forced padding) bit rate (with measurement), if some container padding is present
FrameRate                 : Frames per second
FrameRate/String          : Frames per second (with measurement)
FrameRate_Num             : Frames per second, numerator
FrameRate_Den             : Frames per second, denominator
FrameCount                : Number of frames
Source_FrameCount         : Source Number of frames
Delay                     : Delay fixed in the stream (relative) IN MS
Delay/String              : Delay with measurement
Delay/String1             : Delay with measurement
Delay/String2             : Delay with measurement
Delay/String3             : Delay in format : HH:MM:SS.MMM
Delay/String4             : Delay in format : HH:MM:SS:FF, last colon replaced by semicolon for drop frame if available
Delay/String5             : Delay in format : HH:MM:SS.mmm (HH:MM:SS:FF)
Delay_Settings            : Delay settings (in case of timecode for example)
Delay_DropFrame           : Delay drop frame
Delay_Source              : Delay source (Container or Stream or empty)
Delay_Source/String       : Delay source (Container or Stream or empty)
Delay_Original            : Delay fixed in the raw stream (relative) IN MS
Delay_Original/String     : Delay with measurement
Delay_Original/String1    : Delay with measurement
Delay_Original/String2    : Delay with measurement
Delay_Original/String3    : Delay in format: HH:MM:SS.MMM
Delay_Original/String4    : Delay in format: HH:MM:SS:FF, last colon replaced by semicolon for drop frame if available
Delay_Original/String5    : Delay in format : HH:MM:SS.mmm (HH:MM:SS:FF)
Delay_Original_Settings   : Delay settings (in case of timecode for example)
Delay_Original_DropFrame  : Delay drop frame info
Delay_Original_Source     : Delay source (Stream or empty)
Video_Delay               : Delay fixed in the stream (absolute / video)
Video_Delay/String 
Video_Delay/String1 
Video_Delay/String2 
Video_Delay/String3 
Video_Delay/String4 
Video_Delay/String5 
Video0_Delay              : Deprecated, do not use in new projects
Video0_Delay/String       : Deprecated, do not use in new projects
Video0_Delay/String1      : Deprecated, do not use in new projects
Video0_Delay/String2      : Deprecated, do not use in new projects
Video0_Delay/String3      : Deprecated, do not use in new projects
Video0_Delay/String4      : Deprecated, do not use in new projects
Video0_Delay/String5      : Deprecated, do not use in new projects
TimeStamp_FirstFrame      : TimeStamp fixed in the stream (relative) IN MS
TimeStamp_FirstFrame/Stri : TimeStamp with measurement
TimeStamp_FirstFrame/Stri : TimeStamp with measurement
TimeStamp_FirstFrame/Stri : TimeStamp with measurement
TimeStamp_FirstFrame/Stri : TimeStamp in format : HH:MM:SS.MMM
TimeStamp_FirstFrame/Stri : TimeStamp in format : HH:MM:SS:FF, last colon replaced by semicolon for drop frame if available
TimeStamp_FirstFrame/Stri : TimeStamp in format : HH:MM:SS.mmm (HH:MM:SS:FF)
TimeCode_FirstFrame       : Time code in HH:MM:SS:FF, last colon replaced by semicolon for drop frame if available format
TimeCode_Settings         : Time code settings
TimeCode_Striped          : Time code is striped (only 1st time code, no discontinuity)
TimeCode_Striped/String   : Time code is striped (only 1st time code, no discontinuity)
StreamSize                : Streamsize in bytes
StreamSize/String         : Streamsize in with percentage value
StreamSize/String1 
StreamSize/String2 
StreamSize/String3 
StreamSize/String4 
StreamSize/String5        : Streamsize in with percentage value
StreamSize_Proportion     : Stream size divided by file size
StreamSize_Demuxed        : StreamSize in bytes of hte stream after demux
StreamSize_Demuxed/String : StreamSize_Demuxed in with percentage value
StreamSize_Demuxed/String1 
StreamSize_Demuxed/String2 
StreamSize_Demuxed/String3 
StreamSize_Demuxed/String4 
StreamSize_Demuxed/String : StreamSize_Demuxed in with percentage value (note: theoritical value, not for real use)
Source_StreamSize         : Source Streamsize in bytes
Source_StreamSize/String  : Source Streamsize in with percentage value
Source_StreamSize/String1 
Source_StreamSize/String2 
Source_StreamSize/String3 
Source_StreamSize/String4 
Source_StreamSize/String5 : Source Streamsize in with percentage value
Source_StreamSize_Proport : Source Stream size divided by file size
StreamSize_Encoded        : Encoded Streamsize in bytes
StreamSize_Encoded/String : Encoded Streamsize in with percentage value
StreamSize_Encoded/String1 
StreamSize_Encoded/String2 
StreamSize_Encoded/String3 
StreamSize_Encoded/String4 
StreamSize_Encoded/String : Encoded Streamsize in with percentage value
StreamSize_Encoded_Propor : Encoded Stream size divided by file size
Source_StreamSize_Encoded : Source Encoded Streamsize in bytes
Source_StreamSize_Encoded : Source Encoded Streamsize in with percentage value
Source_StreamSize_Encoded/String1 
Source_StreamSize_Encoded/String2 
Source_StreamSize_Encoded/String3 
Source_StreamSize_Encoded/String4 
Source_StreamSize_Encoded : Source Encoded Streamsize in with percentage value
Source_StreamSize_Encoded : Source Encoded Stream size divided by file size
Title                     : Name of this menu
Language                  : Language (2-letter ISO 639-1 if exists, else 3-letter ISO 639-2, and with optional ISO 3166-1 country separated by a dash if available, e.g. en, en-us, zh-cn)
Language/String           : Language (full)
Language/String1          : Language (full)
Language/String2          : Language (2-letter ISO 639-1 if exists, else empty)
Language/String3          : Language (3-letter ISO 639-2 if exists, else empty)
Language/String4          : Language (2-letter ISO 639-1 if exists with optional ISO 3166-1 country separated by a dash if available, e.g. en, en-us, zh-cn, else empty)
Language_More             : More info about Language (e.g. Director's Comment)
ServiceKind               : Service kind, e.g. visually impaired, commentary, voice over
ServiceKind/String        : Service kind (full)
Disabled                  : Set if that track should not be used
Disabled/String           : Set if that track should not be used
Default                   : Set if that track should be used if no language found matches the user preference.
Default/String            : Set if that track should be used if no language found matches the user preference.
Forced                    : Set if that track should be used if no language found matches the user preference.
Forced/String             : Set if that track should be used if no language found matches the user preference.
AlternateGroup            : Number of a group in order to provide versions of the same track
AlternateGroup/String     : Number of a group in order to provide versions of the same track
 
Image 
Count                     : Count of objects available in this stream
Status                    : bit field (0=IsAccepted, 1=IsFilled, 2=IsUpdated, 3=IsFinished)
StreamCount               : Count of streams of that kind available
StreamKind                : Stream type name
StreamKind/String         : Stream type name
StreamKindID              : Number of the stream (base=0)
StreamKindPos             : When multiple streams, number of the stream (base=1)
StreamOrder               : Stream order in the file, whatever is the kind of stream (base=0)
FirstPacketOrder          : Order of the first fully decodable packet met in the file, whatever is the kind of stream (base=0)
Inform                    : Last **Inform** call
ID                        : The ID for this stream in this file
ID/String                 : The ID for this stream in this file
OriginalSourceMedium_ID   : The ID for this stream in the original medium of the material
OriginalSourceMedium_ID/S : The ID for this stream in the original medium of the material
UniqueID                  : The unique ID for this stream, should be copied with stream copy
UniqueID/String           : The unique ID for this stream, should be copied with stream copy
MenuID                    : The menu ID for this stream in this file
MenuID/String             : The menu ID for this stream in this file
Title                     : Name of the track
Format                    : Format used
Format/String             : Format used + additional features
Format/Info               : Info about Format
Format/Url                : Link
Format_Commercial         : Commercial name used by vendor for theses setings or Format field if there is no difference
Format_Commercial_IfAny   : Commercial name used by vendor for theses setings if there is one
Format_Version            : Version of this format
Format_Profile            : Profile of the Format
Format_Settings_Endianness 
Format_Settings_Packing 
Format_Compression        : Compression method used
Format_Settings           : Settings needed for decoder used
Format_Settings_Wrapping  : Wrapping mode (Frame wrapped or Clip wrapped)
Format_AdditionalFeatures : Format features needed for fully supporting the content
InternetMediaType         : Internet Media Type (aka MIME Type, Content-Type)
CodecID                   : Codec ID (found in some containers)
CodecID/String            : Codec ID (found in some containers)
CodecID/Info              : Info about codec ID
CodecID/Hint              : A hint for this codec ID
CodecID/Url               : A link for more details about this codec ID
CodecID_Description       : Manual description given by the container
Codec                     : Deprecated, do not use in new projects
Codec/String              : Deprecated, do not use in new projects
Codec/Family              : Deprecated, do not use in new projects
Codec/Info                : Deprecated, do not use in new projects
Codec/Url                 : Deprecated, do not use in new projects
Width                     : Width (aperture size if present) in pixel
Width/String              : Width (aperture size if present) with measurement (pixel)
Width_Offset              : Offset between original width and displayed width (aperture size) in pixel
Width_Offset/String       : Offset between original width and displayed width (aperture size)  in pixel
Width_Original            : Original (in the raw stream) width in pixel
Width_Original/String     : Original (in the raw stream) width with measurement (pixel)
Height                    : Height (aperture size if present) in pixel
Height/String             : Height (aperture size if present) with measurement (pixel)
Height_Offset             : Offset between original height and displayed height (aperture size) in pixel
Height_Offset/String      : Offset between original height and displayed height (aperture size)  in pixel
Height_Original           : Original (in the raw stream) height in pixel
Height_Original/String    : Original (in the raw stream) height with measurement (pixel)
PixelAspectRatio          : Pixel Aspect ratio
PixelAspectRatio/String   : Pixel Aspect ratio
PixelAspectRatio_Original : Original (in the raw stream) Pixel Aspect ratio
PixelAspectRatio_Original : Original (in the raw stream) Pixel Aspect ratio
DisplayAspectRatio        : Display Aspect ratio
DisplayAspectRatio/String : Display Aspect ratio
DisplayAspectRatio_Origin : Original (in the raw stream) Display Aspect ratio
DisplayAspectRatio_Origin : Original (in the raw stream) Display Aspect ratio
ColorSpace 
ChromaSubsampling 
Resolution                : Deprecated, do not use in new projects
Resolution/String         : Deprecated, do not use in new projects
BitDepth 
BitDepth/String 
Compression_Mode          : Compression mode (Lossy or Lossless)
Compression_Mode/String   : Compression mode (Lossy or Lossless)
Compression_Ratio         : Current stream size divided by uncompressed stream size
StreamSize                : Stream size in bytes
StreamSize/String 
StreamSize/String1 
StreamSize/String2 
StreamSize/String3 
StreamSize/String4 
StreamSize/String5        : With proportion
StreamSize_Proportion     : Stream size divided by file size
StreamSize_Demuxed        : StreamSize in bytes of hte stream after demux
StreamSize_Demuxed/String : StreamSize_Demuxed in with percentage value
StreamSize_Demuxed/String1 
StreamSize_Demuxed/String2 
StreamSize_Demuxed/String3 
StreamSize_Demuxed/String4 
StreamSize_Demuxed/String : StreamSize_Demuxed in with percentage value (note: theoritical value, not for real use)
Encoded_Library           : Software used to create the file
Encoded_Library/String    : Software used to create the file
Encoded_Library_Name      : Info from the software
Encoded_Library_Version   : Version of software
Encoded_Library_Date      : Release date of software
Encoded_Library_Settings  : Parameters used by the software
Language                  : Language (2-letter ISO 639-1 if exists, else 3-letter ISO 639-2, and with optional ISO 3166-1 country separated by a dash if available, e.g. en, en-us, zh-cn)
Language/String           : Language (full)
Language/String1          : Language (full)
Language/String2          : Language (2-letter ISO 639-1 if exists, else empty)
Language/String3          : Language (3-letter ISO 639-2 if exists, else empty)
Language/String4          : Language (2-letter ISO 639-1 if exists with optional ISO 3166-1 country separated by a dash if available, e.g. en, en-us, zh-cn, else empty)
Language_More             : More info about Language (e.g. Director's Comment)
ServiceKind               : Service kind, e.g. visually impaired, commentary, voice over
ServiceKind/String        : Service kind (full)
Disabled                  : Set if that track should not be used
Disabled/String           : Set if that track should not be used
Default                   : Set if that track should be used if no language found matches the user preference.
Default/String            : Set if that track should be used if no language found matches the user preference.
Forced                    : Set if that track should be used if no language found matches the user preference.
Forced/String             : Set if that track should be used if no language found matches the user preference.
AlternateGroup            : Number of a group in order to provide versions of the same track
AlternateGroup/String     : Number of a group in order to provide versions of the same track
Summary 
Encoded_Date              : The time that the encoding of this item was completed began.
Tagged_Date               : The time that the tags were done for this item.
Encryption 
colour_description_presen : Presence of colour description
colour_primaries          : Chromaticity coordinates of the source primaries
transfer_characteristics  : Opto-electronic transfer characteristic of the source picture
matrix_coefficients       : Matrix coefficients used in deriving luma and chroma signals from the green, blue, and red primaries
colour_description_presen : Presence of colour description
colour_primaries_Original : Chromaticity coordinates of the source primaries
transfer_characteristics_ : Opto-electronic transfer characteristic of the source picture
matrix_coefficients_Origi : Matrix coefficients used in deriving luma and chroma signals from the green, blue, and red primaries
 
Menu 
Count                     : Count of objects available in this stream
Status                    : bit field (0=IsAccepted, 1=IsFilled, 2=IsUpdated, 3=IsFinished)
StreamCount               : Count of streams of that kind available
StreamKind                : Stream type name
StreamKind/String         : Stream type name
StreamKindID              : Number of the stream (base=0)
StreamKindPos             : When multiple streams, number of the stream (base=1)
StreamOrder               : Stream order in the file, whatever is the kind of stream (base=0)
FirstPacketOrder          : Order of the first fully decodable packet met in the file, whatever is the kind of stream (base=0)
Inform                    : Last **Inform** call
ID                        : The ID for this stream in this file
ID/String                 : The ID for this stream in this file
OriginalSourceMedium_ID   : The ID for this stream in the original medium of the material
OriginalSourceMedium_ID/S : The ID for this stream in the original medium of the material
UniqueID                  : The unique ID for this stream, should be copied with stream copy
UniqueID/String           : The unique ID for this stream, should be copied with stream copy
MenuID                    : The menu ID for this stream in this file
MenuID/String             : The menu ID for this stream in this file
Format                    : Format used
Format/String             : Format used + additional features
Format/Info               : Info about Format
Format/Url                : Link
Format_Commercial         : Commercial name used by vendor for theses setings or Format field if there is no difference
Format_Commercial_IfAny   : Commercial name used by vendor for theses setings if there is one
Format_Version            : Version of this format
Format_Profile            : Profile of the Format
Format_Compression        : Compression method used
Format_Settings           : Settings needed for decoder used
Format_AdditionalFeatures : Format features needed for fully supporting the content
CodecID                   : Codec ID (found in some containers)
CodecID/String            : Codec ID (found in some containers)
CodecID/Info              : Info about this codec
CodecID/Hint              : A hint/popular name for this codec
CodecID/Url               : A link to more details about this codec ID
CodecID_Description       : Manual description given by the container
Codec                     : Deprecated
Codec/String              : Deprecated
Codec/Info                : Deprecated
Codec/Url                 : Deprecated
Duration                  : Play time of the stream in ms
Duration/String           : Play time in format : XXx YYy only, YYy omited if zero
Duration/String1          : Play time in format : HHh MMmn SSs MMMms, XX omited if zero
Duration/String2          : Play time in format : XXx YYy only, YYy omited if zero
Duration/String3          : Play time in format : HH:MM:SS.MMM
Duration/String4          : Play time in format : HH:MM:SS:FF, last colon replaced by semicolon for drop frame if available
Duration/String5          : Play time in format : HH:MM:SS.mmm (HH:MM:SS:FF)
Duration_Start 
Duration_End 
Delay                     : Delay fixed in the stream (relative) IN MS
Delay/String              : Delay with measurement
Delay/String1             : Delay with measurement
Delay/String2             : Delay with measurement
Delay/String3             : Delay in format : HH:MM:SS.MMM
Delay/String4             : Delay in format : HH:MM:SS:FF, last colon replaced by semicolon for drop frame if available
Delay/String5             : Delay in format : HH:MM:SS.mmm (HH:MM:SS:FF)
Delay_Settings            : Delay settings (in case of timecode for example)
Delay_DropFrame           : Delay drop frame
Delay_Source              : Delay source (Container or Stream or empty)
List_StreamKind           : List of programs available
List_StreamPos            : List of programs available
List                      : List of programs available
List/String               : List of programs available
Title                     : Name of this menu
Language                  : Language (2-letter ISO 639-1 if exists, else 3-letter ISO 639-2, and with optional ISO 3166-1 country separated by a dash if available, e.g. en, en-us, zh-cn)
Language/String           : Language (full)
Language/String1          : Language (full)
Language/String2          : Language (2-letter ISO 639-1 if exists, else empty)
Language/String3          : Language (3-letter ISO 639-2 if exists, else empty)
Language/String4          : Language (2-letter ISO 639-1 if exists with optional ISO 3166-1 country separated by a dash if available, e.g. en, en-us, zh-cn, else empty)
Language_More             : More info about Language (e.g. Director's Comment)
ServiceKind               : Service kind, e.g. visually impaired, commentary, voice over
ServiceKind/String        : Service kind (full)
ServiceName 
ServiceChannel 
Service/Url 
ServiceProvider 
ServiceProvider/Url 
ServiceType 
NetworkName 
Original/NetworkName 
Countries 
TimeZones 
LawRating                 : Depending on the country it's the format of the rating of a movie (P, R, X in the USA, an age in other countries or a URI defining a logo).
LawRating_Reason          : Reason for the law rating
Disabled                  : Set if that track should not be used
Disabled/String           : Set if that track should not be used
Default                   : Set if that track should be used if no language found matches the user preference.
Default/String            : Set if that track should be used if no language found matches the user preference.
Forced                    : Set if that track should be used if no language found matches the user preference.
Forced/String             : Set if that track should be used if no language found matches the user preference.
AlternateGroup            : Number of a group in order to provide versions of the same track
AlternateGroup/String     : Number of a group in order to provide versions of the same track
Chapters_Pos_Begin        : Used by third-party developers to know about the beginning of the chapters list, to be used by Get(Stream_Menu, x, Pos), where Pos is an Integer between Chapters_Pos_Begin and Chapters_Pos_End
Chapters_Pos_End          : Used by third-party developers to know about the end of the chapters list (this position excluded)
