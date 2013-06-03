from pyral import Rally
import textwrap

def get_rally_connection(USER, PASSWORD, PROJECT, VERSION='1.43', SERVER='rally1.rallydev.com'):
    ''' return a rally connection object '''

    # get the rally connection object
    rally = Rally(SERVER, USER, PASSWORD, version=VERSION, project=PROJECT)
    rally.enableLogging('/tmp/rally.log')

    return rally

def get_rally_artifact_obj(rally_connection_obj, artifact_type, FormattedID):
    ''' return a rally artifact object of type 'artifact_type' '''

    artifact_obj = rally_connection_obj.get(artifact_type, query="FormattedID = %s" % FormattedID, instance=True)
    return artifact_obj

def do_rally_query(
        rally_connection_obj, artifact_type, query=None, limit=None, **kwargs):
    ''' perform a query against the rally api and return the result object '''

    query_obj = rally_connection_obj.get(
        artifact_type, query=query, limit=limit, instance=True, **kwargs)

    return query_obj

def strip_html(text_to_clean):
    ''' remove html tags, wrap to 80 lines, and return clean text
    returns a string '''

    strip_pattern = '<[^<]+?>'
    stripped = textwrap.re.sub(strip_pattern, '', text_to_clean)
    wrapped = textwrap.fill(stripped, 70)
    # truncate to 300 characters
    if len(wrapped) > 300:
        wrapped =  wrapped[:300] + '\n\n...output truncated'

    return wrapped
