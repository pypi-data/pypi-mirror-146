# Memorable

A library for generating memorable strings.

## Usage

```python
import memorable

memorable.name()
# lue-the-jealously-happy-go-lucky
memorable.action()
# eat-a-pretty-payment
memorable.thing()
# cleverly-neglected-talk
memorable.code_phrase()
# amused-chilly-minestrone-distribute
```

## Advanced usage

It is possible to generate strings focusing on a specific theme.

```python
for kind in memorable.NounTypes:
    phrase = memorable.thing(kind=kind)
    print(f'{kind.value}: {phrase}')
    # alcohols: wonderfully-overdue-beer
    # animals: uncritically-thoughtful-octopus
    # elements: vividly-mindless-chromium
    # foods: jubilantly-snappy-stew
    # fruits: poorly-handmade-kiwano
    # geographies: quaintly-mountainous-beach
    # households: hurriedly-ready-zester
    # investments: meticulously-variable-bitcoin
    # literature: madly-bogus-ode
    # mythical: readily-general-centaur
    # occupations: casually-tinted-data-scientist
    # organs: nightly-splendid-lungs
    # places: casually-definitive-farm
    # relations: later-ready-babushka
    # rocks: slavishly-hot-picrite
    # royalty: fast-loyal-despot
    # tools: unnecessarily-unripe-needle-nose
    # transports: hollowly-cheerful-pickup
    # trees: never-offbeat-fir
    # vegtables: naively-happy-bitter-melon
    # water_bodies: upliftingly-flickering-wadi
```

If `memorable` is being used to generate ids and you'd like to reduce the
frequency of collisions (you should expect some collisions) it's possible
to request some extra characters tacked on the end to make them less common.

```python
memorable.action(extra_characters=4)
# demand-the-hidden-bread-machine-gths
```