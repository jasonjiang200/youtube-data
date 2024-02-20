from googleapiclient.discovery import build
def main():
    # Open, read, and extract api key
    API_KEY = open("../config.txt", "r").read().split("=")[1]
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    def get_channel_stats(youtube, channel_info, input_type: str) -> list:
        """
        Inputs: 
            youtube, an instance of the build to make calls with
            channel_info, a list of channel ids to look up, a username, or a handle
            input_type: specifies input type of channel_info 
        Outputs: 
            all_data, a list of dictionaries. Each dictionary contains information about one of the channels.         
        """

        # Classify the request
        if input_type == "id":
            request = youtube.channels().list(
                part='snippet, contentDetails, statistics',
                id=','.join(channel_info))
        elif input_type == "username":
            request = youtube.channels().list(
                part='snippet, contentDetails, statistics',
                forUsername=channel_info)
        elif input_type == "handle":
            # TODO: Look up a YT user by their handle, e.g. @BerkeleyNews
            request = youtube.channels().list(
                part='snippet, contentDetails, statistics',
                forHandle=channel_info)
        response = request.execute()
        if 'items' not in response: # No channels found
            return None
        all_data = [] # The list of dictionaries to be returned
        for i in range(len(response['items'])):
            data = dict(channel_name = response['items'][i]['snippet']['title'], 
                        subscribers = response['items'][i]['statistics']['subscriberCount'],
                        views = response['items'][i]['statistics']['viewCount'],
                        videoCount = response['items'][i]['statistics']['videoCount'],
                        )
            all_data.append(data)
        return all_data
    
    # TODO: Create pdfs based on the data for the channels

    # Initial Test
    x = get_channel_stats(youtube, "BerkeleyNews", "username") 
    print(x)

    
if __name__ == '__main__':
    main()


