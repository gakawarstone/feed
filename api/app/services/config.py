from feedgen.feed import FeedGenerator

fg = FeedGenerator()
fg.title('TEST FEED')
fg.link(href='http://example.com', rel='alternate')
fg.description('d')
