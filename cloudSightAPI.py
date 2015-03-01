#!usr/bin/env python
#encoding=utf-8

import requests
import sys, getopt

LOCALE = 'zh-CN'
LANGUAGE = 'zh-CN'

def makeRequest(imageUrl):
    reqUrlA = 'https://api.cloudsightapi.com/image_requests/' # get token
    reqUrlB = 'https://api.cloudsightapi.com/image_responses/' # get the final recognition result with token

    headers = { 
            'Authorization' : 'CloudSight amZd_zG32VK-AoSz05JLIA',
            'Host' : 'api.cloudsightapi.com',
            'Origin:' : 'https://cloudsightapi.com'
            }

    postData = {
            'image_request[remote_image_url]' : imageUrl,
            'image_request[locale]': LOCALE,
            'image_request[language]': LANGUAGE
            }

    try:
        response = requests.post(reqUrlA, headers=headers, data=postData)
    except Exception, e:
        print 'Error: connection error, please check your Internet and confirm the image url'
        sys.exit()
    
    token = response.json()['token']

    # you may get some response with status 'not completed' for about some times before getting the final result
    reqTimes = 10
    while reqTimes > 0:
        try:
            response = requests.get(reqUrlB + token, headers=headers)
        except Exception, e:
            print 'Error: connection error, please check your Internet and confirm the image url'
            sys.exit()
        status = response.json()['status']
        if status == 'completed':
            print 'RESULT: '
            print '\timage url:', imageUrl
            print '\timage name:', response.json()['name']
            print
            # return response.json()['name']
            break
        elif status == 'not completed':
            print 'recognizing...'
            reqTimes -= 1

def usage():
        print '''
        usage: 
            cloudSightAPI ImageURL
            type `cloudSightAPI -h` to get help
        '''

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'h')
        for op, value in opts:
            if op == '-h':
                usage()
                sys.exit()
            if len(args) == 0:
                usage()
                sys.exit()
    except getopt.GetoptError as e:
        print 'Error: using invalid parameter -%s' % e.opt
        usage()
        sys.exit()

    imageUrl = sys.argv[1]
    makeRequest(imageUrl)

if __name__ == '__main__':
    main()
