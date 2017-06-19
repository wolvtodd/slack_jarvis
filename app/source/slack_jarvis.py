import time
import datetime
import requests
from bs4 import BeautifulSoup
from slackclient import SlackClient

BOT_TOKEN = "xoxb-199461394082-gahzY1m5qKk4igfQa5zsINRy"
GOOGLE_SEARCH_LINK = "https://www.google.com/search?sclient=psy-ab&client=ubuntu&hs=k5b&channel=fs&biw=1366&bih=648&noj=1&q="

def filterJarvisKeyword(msg):
	results = msg.split(' ', )
	if results and results[0] == "jarvis":
		return True
	return False


def filterEventKeyword(msg):
	results = msg.split(' ', )
	if results and (len(results) > 1):
		return results[1]
	return ""


def printHelp(strCommand):
	result = ""
	if strCommand == "help":
		result += "<help>: print this \n"
		result += "<time>: print current date time \n"
		result += "<'contents'>: search on google for contents\n"
		result += "<baiyon>: curse our public enemy in the office \n"
	return result


def respondTime(strCommand):
	if strCommand == "time":
		return "Time: {}".format(datetime.datetime.now())
	return ""


def respondCursingBaiyon(strCommand):
	if strCommand == "baiyon":
		return "He is an annoying stupid useless mud"
	return ""


def respondSearchForKeyword(message):
	result = ""

	searchWords = message.split(" ", 1)
	if (searchWords and len(searchWords) > 1):
		searchWord = searchWords[1]
		goog_search = GOOGLE_SEARCH_LINK + searchWord
		request = requests.get(goog_search)
		soup = BeautifulSoup(request.text, "html.parser")

		result +=soup.find('cite').text

	return result

def respondRandomReply(message):
	result = "Yes, sir?"
	return result


def main():
	sc = SlackClient(BOT_TOKEN)

	if sc.rtm_connect():
		sc.rtm_send_message("bottest", "Jarvis is online.")

		respondText = ""
		while True:
			for slack_message in sc.rtm_read():
				message = slack_message.get("text")
				user = slack_message.get("user")

				if message and user:
					if filterJarvisKeyword(message):
						eventKeyword = filterEventKeyword(message)

						respondText = printHelp(eventKeyword)
						if respondText != "":
							break

						respondText = respondTime(eventKeyword)
						if respondText != "":
							break

						respondText = respondCursingBaiyon(eventKeyword)
						if respondText  != "":
							break

						respondText = respondSearchForKeyword(message)
						if respondText != "":
							break

						respondText = respondRandomReply(message)
						if respondText != "":
							break



			if (respondText != ""):
				sc.rtm_send_message(slack_message.get("channel"), respondText)
				respondText = ""

			time.sleep(0.5)



if __name__ == '__main__':
    main()