import random

class Voting:
    def ejected(name, isImpostor=None, remaining=0):
        '''Creates a message for when the player has been ejected.
        Args:
            name (str): The name of the player who has been ejected.
            isImpostor (bool): Whether the player was an impostor. Use None for a random result.
            remaining (int): The number of remaining players. Default 0.
        Returns:
                str: The message to be displayed.
        '''
        if isImpostor is None:
            isImpostor = random.choice([True, False])
        
        if isImpostor:
            return f'''{name} was the Impostor.
            {remaining} Impostors remain.'''
        elif isImpostor != True:
            return f'''{name} was not the Impostor.
            {remaining} Impostors remain.'''

    def ejected_noconf(name):
        '''Creates a message for when the player has been ejected, but the game has confirmations off.
        Args:
            name (str): The name of the player who has been ejected.
        Returns:
                str: The message to be displayed.
        '''
        return f'{name} was ejected.'