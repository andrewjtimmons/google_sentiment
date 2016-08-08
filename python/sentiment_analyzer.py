import argparse
from googleapiclient import discovery
import httplib2
import json
from oauth2client.client import GoogleCredentials
import sys

DISCOVERY_URL = ('https://{api}.googleapis.com/'
                 '$discovery/rest?version={apiVersion}')

def main(text_file):
  with open(text_file) as f:
    text = f.read()

  #get sentiment for individual lines and write it out
  analyzed_lines = []

  for line in text.split('\n'):
    analyzed_lines.append({})
    analyzed_lines[-1]['text'] = line
    analyzed_lines[-1]['analysis'] = anaylze_content(line)

  with open('%s_lines_analyzed.json' % text_file[0:text_file.find('.')], 'wb') as f:
    json.dump(analyzed_lines, f)

def anaylze_content(text):
  '''Run a sentiment analysis request on text.
  This function is a modified version of the tutorial at this link on 7/24/16
  https://cloud.google.com/natural-language/docs/sentiment-tutorial
  '''

  http = httplib2.Http()

  credentials = GoogleCredentials.get_application_default().create_scoped(
      ['https://www.googleapis.com/auth/cloud-platform'])
  http=httplib2.Http()
  credentials.authorize(http)

  service = discovery.build('language', 'v1beta1',
                            http=http, discoveryServiceUrl=DISCOVERY_URL)

  service_request = service.documents().annotateText(
    body={
            "document":{
              "type":"PLAIN_TEXT",
              "content": text
            },
            "features":{
              "extractDocumentSentiment":True
            },
            "encodingType":"UTF8"
          })

  try:
    response = service_request.execute()
    return response
  except:
    # Normally you don't want to catch all errors but what is a side project
    # without tech debt.
    return {"error_msg": str(sys.exc_info()[1])}


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument(
    'text_file', help='The filename of the text you want to analyze.')
  args = parser.parse_args()
  main(args.text_file)