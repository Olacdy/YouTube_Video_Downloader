from hurry.filesize import size, alternative
from pytube import Stream


def get_name_from_stream(stream: Stream) -> str:
    name: str = ""
    name += stream.default_filename.split(".")[1].capitalize() + " "
    try:
        name += stream.resolution + " "
    except:
        pass
    name += size(stream.filesize_approx, system=alternative)
    if stream.includes_audio_track:
        pass
    else:
        name += " No audio"
    return name or "No name"
