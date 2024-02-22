         
            elif bulletsCount == 0 or prayFramesUpdating >= FPS * 5:  # or 5 sec & goose.alive == True
                goose.flyAway()
                dog.laughing()
                if hunterStartTime is None:
                    hunterStartTime = time.time()