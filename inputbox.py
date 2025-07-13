import pygame

def ask(screen, question, font_size=24, font_color=(255, 255, 255), box_color=(0, 0, 0), active_color=(0, 191, 255)):
    pygame.font.init()
    font = pygame.font.Font(None, font_size)
    clock = pygame.time.Clock()

    input_text = ""
    active = True

    box_width = 400
    box_height = 50
    screen_rect = screen.get_rect()
    input_rect = pygame.Rect(
        (screen_rect.width - box_width) // 2,
        (screen_rect.height - box_height) // 2,
        box_width,
        box_height
    )

    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return input_text
                elif event.key == pygame.K_ESCAPE:
                    return None
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

        screen.fill((0, 0, 0))

        pygame.draw.rect(screen, box_color, input_rect)
        pygame.draw.rect(screen, active_color, input_rect, 2)

        question_surf = font.render(question, True, font_color)
        screen.blit(question_surf, (input_rect.x, input_rect.y - 30))

        text_surface = font.render(input_text, True, font_color)
        screen.blit(text_surface, (input_rect.x + 10, input_rect.y + 10))

        pygame.display.flip()
        clock.tick(30)
# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass
