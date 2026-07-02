import sys
from html.parser import HTMLParser

class NestingHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.errors = []
        # Tags that do not require closing tags in HTML5
        self.void_tags = {
            'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
            'link', 'meta', 'param', 'source', 'track', 'wbr'
        }

    def handle_starttag(self, tag, attrs):
        if tag not in self.void_tags:
            line, col = self.getpos()
            self.stack.append((tag, line, col))

    def handle_endtag(self, tag):
        if tag in self.void_tags:
            return  # Void tags shouldn't have closing tags, but if they do, ignore or flag
        
        if not self.stack:
            line, col = self.getpos()
            self.errors.append(f"Unexpected closing tag </{tag}> at line {line}, col {col} (no open tags in stack)")
            return

        expected_tag, o_line, o_col = self.stack.pop()
        if expected_tag != tag:
            line, col = self.getpos()
            self.errors.append(
                f"Mismatched closing tag </{tag}> at line {line}, col {col}. "
                f"Expected </{expected_tag}> (opened at line {o_line}, col {o_col})"
            )
            # Try to recover by popping until we find a match, or push back the popped tag
            # For simplicity, we just report and don't try complex recovery, but we can do a simple check:
            # Let's find the tag in the stack
            found = False
            for idx in range(len(self.stack) - 1, -1, -1):
                if self.stack[idx][0] == tag:
                    # Found it, we closed some tags implicitly or incorrectly
                    unclosed = self.stack[idx+1:] + [(expected_tag, o_line, o_col)]
                    for utag, ul, uc in reversed(unclosed):
                        self.errors.append(f"Implicitly closing unclosed tag <{utag}> opened at line {ul}, col {uc}")
                    self.stack = self.stack[:idx]
                    found = True
                    break
            if not found:
                # Put the expected tag back on stack, ignore this closing tag
                self.stack.append((expected_tag, o_line, o_col))

    def check_unclosed(self):
        while self.stack:
            tag, line, col = self.stack.pop()
            self.errors.append(f"Unclosed tag <{tag}> opened at line {line}, col {col}")

if __name__ == '__main__':
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    parser = NestingHTMLParser()
    parser.feed(content)
    parser.check_unclosed()

    if parser.errors:
        print(f"Found {len(parser.errors)} HTML nesting errors:")
        for err in parser.errors:
            print(f" - {err}")
        sys.exit(1)
    else:
        print("HTML tag nesting is perfectly clean!")
        sys.exit(0)
