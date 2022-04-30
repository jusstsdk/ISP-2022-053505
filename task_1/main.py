import os.path
import re


def get_text(path):
    if not os.path.exists(path):
        print("The file doesn't exit")
        exit()
    elif not os.path.getsize(path):
        print("The file is empty")
        exit()

    with open(path, "r") as file:
        file = file.read()

    return file


def format_text(text):
    text = text.lower()
    for symbol in ".!?-():;,\'\"":
        text = text.replace(symbol, "")
    return text


def get_words_dict(text):
    words_dict = dict()

    for word in format_text(text).split():
        words_dict.setdefault(word, 0)
        words_dict[word] += 1

    return words_dict


def average_in_sentence(text):
    count_of_sentences = len(re.split("[.?!]", text))
    count_of_words = len(text.split())
    return count_of_words / count_of_sentences


def words_in_sentence(text):
    sentence_list = re.split("[.?!]", text)
    words_count_list = list()

    for sentence in sentence_list:
        words_count_list.append(len(sentence.split()))

    return words_count_list


def median_in_sentence(text):
    words_list = words_in_sentence(text)
    words_list.sort()

    length = len(words_list) / 2
    if length % 2 == 0:
        return (words_list[int(length - 1)] + words_list[int(length)]) / 2
    else:
        return words_list[int(length)]


def top_ngrams(text, k, n):
    words_dict = get_words_dict(text)
    sorted_tuples = sorted(words_dict.items(), key=lambda x: x[1], reverse=True)
    sorted_dict = dict(sorted_tuples)
    copy_sorted_dict = sorted_dict.copy()

    for key in copy_sorted_dict:
        if len(key) != n:
            del sorted_dict[key]

    return list(sorted_dict.keys())[:k]


def output_text(file):
    print(file)


def output_stats_about_duplicates(file):
    print('How many times each word is repeated:')
    for key, value in get_words_dict(file).items():
        print(key, value)


def output_average_number(file):
    print(f'Average number of words in a sentence: {average_in_sentence(file)}')


def output_median_number(file):
    print(f'Median number of words in a sentence: {median_in_sentence(file)}')


def check_agrs():
    choice = int(input('Wanna use default k-n values? (1/0) '))

    if choice != 1:
        print('How many n-grams you wanna see?(k)')
        k = int(input())
        print('Enter length of n-grams(n)')
        n = int(input())
        return k, n
    else:
        return 10, 4


def output_top_ngrams(file):
    k, n = check_agrs()
    print('Top n-grams:')
    print(top_ngrams(file, k, n))


def main_menu(path):
    statement = True
    file = get_text(path)

    options_dict = {
        1: output_text,
        2: output_stats_about_duplicates,
        3: output_average_number,
        4: output_median_number,
        5: output_top_ngrams
    }

    while statement:
        print('\n0 - Exit')
        print('1 - Source text')
        print('2 - Stats about duplicates')
        print('3 - Average number of words in a sentence')
        print('4 - Median number of words in a sentence')
        print('5 - Top-K Ngrams\n')

        try:
            user_input = int(input('Your Choice: '))
        except ValueError:
            print('Only integers allowed!')
            continue

        if user_input == 0:
            break
        elif user_input < 0 or user_input > 5:
            print('Dude, read more closely')
            continue
        else:
            options_dict[user_input](file)


def main(path):
    main_menu(path)


if __name__ == '__main__':
    main("text.txt")
