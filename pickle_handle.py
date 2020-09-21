import pickle

def get_pickle(username):
    pickle_in = open('users/' + username + '.pickle', 'rb')
    user = pickle.load(pickle_in)
    pickle_in.close()
    return user

def save_pickle(user):
    pickle_out = open('users/' + user.username + ".pickle", "wb")
    pickle.dump(user, pickle_out)
    pickle_out.close()