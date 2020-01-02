from linebot.models import (
    CarouselContainer, BubbleContainer, URIAction, ImageComponent, BoxComponent, TextComponent, SeparatorComponent
)

# 透過搜尋下來的書，回傳一個 CarouselContainer
def generate_carousel_for_search(books):
    contents = []
    for book in books:
        content = BubbleContainer(
            action=URIAction(uri=book['url']),
            size='micro',
            hero=ImageComponent(
                url=book['photo_url'],
                size='full',
                aspect_mode='cover',
                aspect_ratio='320:213'
            ),
            body=BoxComponent(
                layout='vertical',
                spacing='sm',
                padding_all='13px',
                contents=[
                    TextComponent(text=book['name'], weight='bold', size='sm'),
                    BoxComponent(
                        layout='baseline',
                        contents=[
                            TextComponent(text=book['authors'], size='xs', color='#8c8c8c', margin='md'),
                            TextComponent(text=book['publisher'], size='xs', color='#8c8c8c', margin='md')
                        ]
                    ),
                    SeparatorComponent(margin='md', color='#a0a0a0'),
                    TextComponent(text=book['summary'], color='#8c8c8c', size='xs', wrap=True)
                ]
            ), 
            footer=BoxComponent(
                layout='vertical',            
                contents=[
                    SeparatorComponent(margin='md', color='#a0a0a0'),
                    TextComponent(text=book['price'], wrap=True, size='sm', flex=5, align='center')
                ]
            )
        )
        contents.append(content)
    return CarouselContainer(contents=contents)

# 透過搜尋的關鍵字，回傳一個 BubbleContainer
def generate_search_bubble_from_key(key):
    search_bubble = BubbleContainer(
        body=BoxComponent(
            layout='vertical',
            contents=[
                TextComponent(
                    text='更多 {} 的搜尋結果'.format(key),
                    action=URIAction(uri='https://search.books.com.tw/search/query/key/{}/cat/BKA'.format(key))
                )
            ]
        )
    )
    return search_bubble

# 透過爬下來的排行榜，回傳一個 CarouselContainer
def generate_carousel_for_top10(books):
    contents = []
    for book in books:
        content = BubbleContainer(
            action=URIAction(uri=book['url']),
            size='micro',
            header=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(text='TOP ' + book['no'],
                                  weight='bold', size='lg', align='center'),
                    SeparatorComponent(margin='md', color='#a0a0a0')
                ]
            ),
            hero=ImageComponent(
                url=book['photo_url'],
                size='full',
                aspect_mode='cover'                
            ),
            body=BoxComponent(
                layout='vertical',
                spacing='sm',
                padding_all='13px',
                contents=[
                    TextComponent(text=book['name'], weight='bold', size='sm', align='center', wrap=True),
                    TextComponent(text=book['authors'], size='sm', color='#8c8c8c', margin='md', align='center')                    
                ]
            ), 
            footer=BoxComponent(
                layout='vertical',            
                contents=[
                    SeparatorComponent(margin='md', color='#a0a0a0'),
                    TextComponent(text=book['price'], wrap=True, size='sm', flex=5, align='center')
                ]
            )
        )
        contents.append(content)
    return CarouselContainer(contents=contents)