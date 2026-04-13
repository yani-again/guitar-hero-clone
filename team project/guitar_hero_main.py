
import pygame
import sys
pygame.init()

#window initialisation
pygame.init()
background_colour = ("#FFFFFF")
width = 411
height = 507
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Guitar Hero')
screen.fill(background_colour)

#text customise
smallfont = pygame.font.SysFont('Pixel',50)
colour ='#000000'

#asset definition
game_screen_background = pygame.image.load('game_screen_background.png')
game_screen_background = pygame.transform.scale_by(game_screen_background, 0.96)
song_select_background = pygame.image.load('song_select_background.png')
song_select_background_V2 = pygame.image.load('song_select_background_v2.png')
song_select_background_V2 = pygame.transform.scale_by(song_select_background_V2, 1.55)
menu_background = pygame.image.load('menu_background.png')
menu_background = pygame.transform.scale_by(menu_background, 0.944)
game_over_background = pygame.image.load('game_over_background.png')
game_over_background = pygame.transform.scale_by(game_over_background, 0.92)
replay_background = pygame.image.load('replay_background.png')
replay_background = pygame.transform.scale_by(replay_background, 0.96)

lanez_hover = pygame.image.load('lanez_hover.png')
lanez_plain = pygame.image.load('lanez_plain.png')
lanez_hover = pygame.transform.scale_by(lanez_hover, 0.5)
lanez_plain = pygame.transform.scale_by(lanez_plain, 0.5)
lanez_hover_rect = pygame.Rect(192,180, 440, 40)
lanez_cover = pygame.image.load('lanez_cover.png')
lanez_cover = pygame.transform.scale_by(lanez_cover, 0.5)
lanez_character = pygame.image.load('atlantic_character.png')
lanez_character = pygame.transform.scale_by(lanez_character, 0.167)

weeknd_hover = pygame.image.load('weeknd_hover.png')
weeknd_plain = pygame.image.load('weeknd_plain.png')
weeknd_hover = pygame.transform.scale_by(weeknd_hover, 0.5)
weeknd_plain = pygame.transform.scale_by(weeknd_plain, 0.5)
weeknd_hover_rect = pygame.Rect(192,230, 440, 40)
weeknd_cover = pygame.image.load('weeknd_cover.png')
weeknd_cover = pygame.transform.scale_by(weeknd_cover, 0.5)
weeknd_character = pygame.image.load('atlantic_character.png')
weeknd_character = pygame.transform.scale_by(weeknd_character, 0.167)

impala_plain = pygame.image.load('impala_plain.png')
impala_hover = pygame.image.load('impala_hover.png')
impala_hover = pygame.transform.scale_by(impala_hover, 0.5)
impala_plain = pygame.transform.scale_by(impala_plain, 0.5)
impala_hover_rect = pygame.Rect(192,280, 440, 36)
impala_cover = pygame.image.load('impala_cover.png')
impala_cover = pygame.transform.scale_by(impala_cover, 0.5)
impala_character = pygame.image.load('impala_character.png')
impala_character = pygame.transform.scale_by(impala_character, 0.067)

tvgirl_hover = pygame.image.load('tvgirl_hover.png')
tvgirl_plain = pygame.image.load('tvgirl_plain.png')
tvgirl_hover = pygame.transform.scale_by(tvgirl_hover, 0.5)
tvgirl_plain = pygame.transform.scale_by(tvgirl_plain, 0.5)
tvgirl_hover_rect = pygame.Rect(192,330, 440, 36)
tvgirl_cover = pygame.image.load('tvgirl_cover.png')
tvgirl_cover = pygame.transform.scale_by(tvgirl_cover, 0.5)
tvgirl_character = pygame.image.load('tvgirl_character.png')
tvgirl_character = pygame.transform.scale_by(tvgirl_character, 0.14)

atlantic_plain = pygame.image.load('atlantic_plain.png')
atlantic_hover = pygame.image.load('atlantic_hover.png')
atlantic_plain = pygame.transform.scale_by(atlantic_plain, 0.5)
atlantic_hover = pygame.transform.scale_by(atlantic_hover, 0.5)
atlantic_hover_rect = pygame.Rect(192,380, 440, 36)
atlantic_cover = pygame.image.load('atlantic_cover.png')
atlantic_cover = pygame.transform.scale_by(atlantic_cover, 0.5)
atlantic_character = pygame.image.load('atlantic_character.png')
atlantic_character = pygame.transform.scale_by(atlantic_character, 0.167)

note = pygame.image.load('note.png')
note = pygame.transform.scale_by(note, 0.24)

time_bar = pygame.Rect(49, 470, 20, 23)




#song select button dictionary
songs_select_buttons = {
    'lanez': {
        'rect': lanez_hover_rect,
        'y': 180,
        'hover_img': lanez_hover,
        'plain_img': lanez_plain,
        'cover_img': lanez_cover,
        'character_img': lanez_character
    },
    'weeknd': {
        'rect': weeknd_hover_rect,
        'y': 230,
        'hover_img': weeknd_hover,
        'plain_img': weeknd_plain,
        'cover_img': weeknd_cover,
        'character_img': weeknd_character
    },
    'impala': {
        'rect': impala_hover_rect,
        'y': 280,
        'hover_img': impala_hover,
        'plain_img': impala_plain,
        'cover_img': impala_cover,
        'character_img': impala_character
    },
    'tvgirl': {
        'rect': tvgirl_hover_rect,
        'y': 330,
        'hover_img': tvgirl_hover,
        'plain_img': tvgirl_plain,
        'cover_img': tvgirl_cover,
        'character_img': tvgirl_character
    },
    'atlantic': {
        'rect': atlantic_hover_rect,
        'y': 380,
        'hover_img': atlantic_hover,
        'plain_img': atlantic_plain,
        'cover_img': atlantic_cover,
        'character_img': atlantic_character
    }
}

#songs dictionary
songs = {
    'lanez': {
        'file': 'Tory Lanez - The Color Violet.mp3',
        'length': 226
    },
    'weeknd': {
        'file': 'The Weeknd - Starboy ft. Daft Punk.mp3',
        'length': 230
    },
    'impala': {
        'file': 'Tame Impala - The Less I Know The Better.mp3',
        'length': 217
    },
    'tvgirl': {
        'file': 'TV Girl - Lovers Rock.mp3',
        'length': 207
    },
    'atlantic': {
        'file': 'Chase Atlantic - Into It.mp3',
        'length': 15
    }
}
#204

#notes position definition
notes_y = {'red_y' : 55,
        'blue_y' : 55,
        'green_y' : 55,
        'yellow_y' : 55,
        'orange_y' : 55}

#song charts
charts = {
  'lanez': [],
  'weeknd': [],
  'impala': [],
  'tvgirl': [],
  'atlantic': []
}

#clock initialise
clock = pygame.time.Clock()
song_select_button = pygame.Rect(80, 430, 100, 40) 

#program loop
run = True
screen_flag = 'menu'
song_choice = ''
while run:
    mouse = pygame.mouse.get_pos()
    #event detection loop
    for event in pygame.event.get():
    
    #program exit
        if event.type == pygame.QUIT:
          run = False
          pygame.quit()
          sys.exit()


        #menu screen
        if screen_flag == 'menu':
            pygame.draw.rect(screen, "#FFFFFF", song_select_button)
            screen.blit(menu_background, (0,0))
            #detects mouse button down     
            if event.type == pygame.MOUSEBUTTONDOWN:
                if song_select_button.collidepoint(mouse):
                    screen_flag = 'song_select'    

        #song select screen
        if screen_flag == 'song_select':
            back_button = pygame.Rect(305, 466, 90, 20)
            pygame.draw.rect(screen, '#ffffff', back_button)
            pygame.draw.rect(screen,'#ffffff', atlantic_hover_rect)
            pygame.draw.rect(screen,'#ffffff', impala_hover_rect)
            pygame.draw.rect(screen,'#ffffff', lanez_hover_rect)
            pygame.draw.rect(screen,'#ffffff', tvgirl_hover_rect)
            pygame.draw.rect(screen,'#ffffff', weeknd_hover_rect)
            screen.blit(song_select_background,(0,0))
            #back to menu screen button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(mouse):
                    screen_flag = 'menu'
            #different song buttons
            #song buttons
            for name, data in songs_select_buttons.items():
                #detect mouse hover on button
                if data['rect'].collidepoint(mouse):
                    screen.blit(data['hover_img'], (190, data['y']))
                    screen.blit(data['cover_img'], (30, 170))
                    screen.blit(data['character_img'], (30, 320))
                    #detects mouse click on button
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        screen_flag = 'game_screen'
                        song_choice = name
                        #plays song when game screen (had to be here instead of 
                        #gamescreen section cause event loop) TROUBLESHOOTED
                        pygame.mixer.music.load(songs[song_choice]['file'])
                        pygame.mixer.music.play()
                #draws plain button when mouse no longer hovers button
                else:
                    screen.blit(data['plain_img'], (190, data['y']))
      
      
    #gamescreen
    if screen_flag == 'game_screen':
        screen.blit(game_screen_background,(0,0))
        #intialises time bar
        pygame.draw.rect(screen, "#1F9425", time_bar, width = 0, border_radius = 15)
        #temporary for demonstration: draws notes to screen
        screen.blit(note, (104,notes_y['green_y']))
        screen.blit(note, (150, notes_y['red_y']))
        screen.blit(note, (196, notes_y['yellow_y']))
        screen.blit(note, (240, notes_y['blue_y']))
        screen.blit(note, (284, notes_y['orange_y']))
        #temporary for demonstration: moves notes down 
        #screen until bottom and resets position
        for name, y in notes_y.items():
            if notes_y[name] >= 368:
                notes_y[name] = 55
            else:
                notes_y[name] += 1
        
        #retrieves time of song
        current_time = pygame.mixer.music.get_pos() / 1000
        song_length = float(songs[song_choice]['length'])
        progress = current_time / song_length
        #progression of timebar and end of game detection
        if current_time <= song_length: 
            time_bar.width = progress * 319 + 10
        else:
            pygame.mixer.music.stop()
            screen_flag = 'game_over'

    #gameover screen
    if screen_flag == 'game_over':
        next_button = pygame.Rect(149, 398, 90, 30)
        pygame.draw.rect(screen, '#ffffff', next_button)
        screen.blit(game_over_background, (0,0))
        if event.type == pygame.MOUSEBUTTONDOWN:
            if next_button.collidepoint(mouse):
                screen_flag = 'replay'
        #game score to be added here
        
    #replay screen 
    if screen_flag == 'replay':
        menu_button = pygame.Rect(250, 376, 90, 30)
        pygame.draw.rect(screen, '#ffffff', menu_button)
        replay_button = pygame.Rect(114, 149, 90, 30)
        pygame.draw.rect(screen, '#ffffff', replay_button)
        screen.blit(replay_background, (0,0))
        #detects button interaction and changes screens
        if event.type == pygame.MOUSEBUTTONDOWN:
            if menu_button.collidepoint(mouse):
                screen_flag = 'menu'
        if event.type == pygame.MOUSEBUTTONDOWN:
            if replay_button.collidepoint(mouse):
                screen_flag = 'game_screen'
                #plays song for replay of game (here and not gamescreen section because of eventlooping)
                pygame.mixer.music.load(songs[song_choice]['file'])
                pygame.mixer.music.play()

    #updates display screen every loop
    pygame.display.update()
    clock.tick(60)
