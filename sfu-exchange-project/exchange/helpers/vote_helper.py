def processNewVoteActionOnUpvotedPost(voteObject, isUpvoteClicked, currentUserVote, user):
    if isUpvoteClicked:
        voteObject.votes = voteObject.votes - 1
        voteObject.voted.remove(user)
        voteObject.save()
        voteObject.refresh_from_db()
        currentUserVote.delete()
    else: 
        # Because we already have a existing upvote, we need to -1 to negate existing upvote and -1 for the downvotw
        voteObject.votes = voteObject.votes - 2
        voteObject.save()
        currentUserVote.is_upvote = False
        currentUserVote.save()

def processNewVoteActionOnDownvotedPost(voteObject, isUpvoteClicked, currentUserVote, user):
    if isUpvoteClicked:
        voteObject.votes = voteObject.votes + 2
        voteObject.save()
        currentUserVote.is_upvote = True
        currentUserVote.save()
    else:
        voteObject.votes = voteObject.votes + 1
        voteObject.voted.remove(user)
        voteObject.save()
        voteObject.refresh_from_db()
        currentUserVote.delete()