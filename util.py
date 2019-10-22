import discord
import random
import praw
import config

# reddit = praw.Reddit(client_id=config.REDDIT_ID, client_secret=config.REDDIT_SECRET,user_agent=config.USER_AGENT)

# multireddit = 'memes'
# sub = reddit.subreddit(multireddit)


def dice_roller(ctx, arg):
    # contents = arg.content[len("!r"):]
    contents = arg.lower()  # make the contents of the argument lowercase
    # word_list = contents.split(" ")

    output = ctx.author.mention  # Start output with user name
    output += " `" + contents.replace(" ", "") + "` "  # Add the arguments to the output
    summation = 0  # Establish a sum  counter track the sum of the rolls
    # for word in word_list:
    roll_word = contents.split('d')  # Split argument into two parts at the d
    if len(roll_word) > 1:  # If there are more than one components
        output += "("
        for x in range(0, int(roll_word[0])):  # Loop it based on the number of dice
            rand_int = random.randint(1,  int(roll_word[1]))  # Create a random integer based on the number of sides
            output += str(rand_int)  # Add the roll to the output addition section
            if x is not int(roll_word[0]) - 1:  # Add a + if we are not at the end of the loop
                output += ' + '
            summation += rand_int  # Add the new int to the total sum
        output += ") "
    else:
        if roll_word[0].isdigit() is True:
            output = output.strip()
            output += ' + ' + str(roll_word[0])
            summation += int(roll_word[0])
    output += " = " + str(summation)  # Add the sum to the output string
    return output


def test(ctx):
    output = "test1234"
    return output

#def meme(ctx):
    #post = sub.random()
   # msg = "{}\nSource: {}".format(post.url, post.permalink)
   # return msg
   
# define function for creating initial vote
def vote_start(question, choices_arr, emojis):
    print("Vote is being made...")
    
    # create embed
    vote_announce = discord.Embed(title="Time for a vote!")
    vote_announce.add_field(name = "Question", value = question) # add question field to embed
    
    # assign emojis to choices as a string and add to embed
    choices_string = ""
    i = 0
    while i < len(choices_arr): # until all choices have been assigned
        choices_string += (emojis[i] + "" + choices_arr[i] + "\n")
        i +=1 # append to string that will be displayed in embed
    vote_announce.add_field(name = "Choices", value = choices_string)
    
    # return embedded vote announcement
    return vote_announce

# define function for counting the votes
def tally_up(question, choices_arr, message):
    
    vote_string = "vote" # singular or plural amount of votes?
    tie_flag = 0 # was there a tie?
    
    # tally dictionary
    tallies = {react.emoji: react.count for react in message.reactions}
    
    # check for a tie
    tallies_sorted = sorted(tallies.values(), reverse=True) # sort highest numbers
    if tallies_sorted[0] != tallies_sorted[1]: # if there is only one maximum, find the winner
        winner_count = max(tallies.values()) - 1 # assign winner count
        winner_emoji = max(tallies, key = tallies.get) # assign winner emoji
    
        winner = choices_arr[list(tallies.keys()).index(winner_emoji)] # assign winner using the index of winner_emoji
    
        # if more than one vote or no votes, change string to votes
        if winner_count > 1 or winner_count == 0: #
            vote_string = "votes"
        
    else: # there's a tie
        tie_flag = 1
        
    
    vote_winner = discord.Embed(title="We have a winner!")
    if tie_flag == 0: # add field based on whether there's a tie or not
        vote_winner.add_field(name = "And your winner is...", value = 
                          "__**" + winner + "**__ (" + winner_emoji + ")" +
                          " with __**" + str(winner_count) + "**__ " + vote_string + "!")
    else:
        vote_winner.add_field(name = "And your winner is...", value = 
                          "No one! It's a tie!")
    
    return vote_winner

def cmd_help(ctx):
    output = "Command: test ---- Arguments: None. ---- Function: Sends a test post"
    output += "\nCommand: roll ---- Arguments: XdY. X = # of dice, Y = # or sides per die. ---- Function: rolls dice"
    output += "\nCommand: meme ---- Arguments: None. ---- Function: Posts a meme from Redit"
    return output
