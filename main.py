from pinout import LEDSTRIP



    
def main():
    # modules:
    # Comms with server
    # MotionCtrl
    # Logging
    # Camera / Comp Vision
    # 
    
    # Terminology: Server == External opponent
    # User == Physical player

    ########### LOOP:
    # Check for incoming messages
    # (Send outgoing messages?)

    #== FSM?
    ### State: Initial state:
    #   Setup internet connection and threads...
    #   Enter Wait for user input
    #
    ### State: Wait for user input:
    #   Wait for user input...
    # 
    ### State: Wait for server move
    #   Be able to exit..?
    #   Still to health check (if safety is importantes)
    #   If two server players, do not enter user move mode.
    # 
    ### State: Wait for user to move
    #   Poll comp vision to know move is done? Or user hit btn to say I have moved?
    #   Send move to server
    #   Enter wait for server, if two user players do not enter wait for server
    #
    ### State: Board reset
    #   Somehow enter board reset
    #   Reset board
    #   Enter wait for user input
    #== END FSM
    # Let pcu breathe...
    ########### END LOOP
    
    " main "
    return

if __name__ == '__main__':
    main()
