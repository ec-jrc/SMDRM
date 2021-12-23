

def extend_text_field(data: dict) -> str:
    """Extend text of original tweet with nested search."""
    try:
        text = data['retweeted_status']['extended_tweet']['full_text']
    except:
        # Try for extended text of an original tweet, if RT'd (REST API)
        try:
            text = data['retweeted_status']['full_text']
        except:
            # Try for extended text of an original tweet (streamer)
            try:
                text = data['extended_tweet']['full_text']
            except:
                # Try for extended text of an original tweet (REST API)
                try:
                    text = data['full_text']
                except:
                    # Try for basic text of original tweet if RT'd
                    try:
                        text = data['retweeted_status']['text']
                    except:
                        # Try for basic text of an original tweet
                        try:
                            text = data['text']
                        except:
                            # Nothing left to check for
                            text = ''
    return text
