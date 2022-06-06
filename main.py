from lib.game import Game

# Global constants defining the minimal and maximal search time allowed
MIN_TIME_S = 5
MAX_TIME_S = 90


def main():
    # Print welcome message
    print('\nWelcome to Set! You play the computer, so it\'s effectively a race against the clock.'
          '\nYou can pick your desired difficulty by choosing an appropriate time you are allowed '
          'to search.\n')

    search_time_s = None

    # Prompt user to enter search time, validating input
    while search_time_s is None:
        search_time_str = input('Please enter your search time (s): ')

        try:
            value = int(search_time_str)

            if value <= 0:
                print(f'Haha, think you are funny? Accepted inputs are in the range [{MIN_TIME_S}, '
                      f'{MAX_TIME_S}]')
            elif value < MIN_TIME_S:
                print(f'Don\'t be too hard on yourself, enter a minimum of {MIN_TIME_S}!')
            elif value > MAX_TIME_S:
                print(f'Come on, that\'s too easy, enter a maximum of {MAX_TIME_S}!')
            else:
                search_time_s = value
        except ValueError:
            print('Please enter an integer!')

    print('\nHave fun!\n')

    # Start game with user-set search time
    game = Game(search_time_s * 1000)
    game.start()


if __name__ == '__main__':
    main()
