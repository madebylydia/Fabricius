# Fabricius

Fabricius - A Python 3.10 Project Template engine with superpowers!

> :warning: Fabricius is a work in progress! Please, play with it with a grain of salt; expect bugs, crashes, non-documented portion of the application & more unexpected behavior.

Documentation: <https://fabricius.readthedocs.io>

> :warning: Fabricius still does not comes with it's CLI tool! It is a work in progress!

## Project Status Update

Hi! Fabricius's developer writing.

This is to report how things are going for Fabricius, maybe it get interest for some peoples, or not, well, whoever you might be, if you're reading this, thanks for passing by :)

I've been pretty busy recently with life, many things are changing in my life that make poorly available for some free time and I don't have much time to code recently, I try to from time-to-time, but it's rare.
I've also had some trouble about considering how Fabricius should be built, I don't think the way I've built it is the right way, and I always question myself on how right should things be. I'm happy with certain things, but the overall layout of the application just doesn't feel right to me.

Not that I'm into a full rewrite, but I want to rework the way I'm building the application, and that takes time and a lot of consideration about how to handle things again.

Maybe when I have some free time again, I will do stuff here and there, but I really don't want to give promises about the future of this application. I'm considering of switching languages to something more "mature" and interesting to me, plus that I've lost the reason why I was building this app in the end, but it's not a big change to me.

So overall, Fabricius is more or less frozen for the time being because of my personal life. I wish I could make this app ASAP and deliver it to everyone as to release a work I've been very hyped to work on.

I'm not particularly interested in someone else taking up my work (If any??) but... there's a license so... if I ever don't keep up... code's here!

Thanks for reading, apologizes for these little words, but I hope to "be back" soon enough!

## Goals

1. Create a working project from a project template
2. Create a fully working CLI using Rich
3. Ability to clone repository and use their templates
4. Create a secure tool (Do not allow unsecure scripts)
5. Create a fully type hinted tool

## Why the name of "Fabricius"?

I am an immense fan of roman names, and I very often name my project after a meaningful roman name.

"Fabricius" (In French, "Artisan") is translated to "craftsman", which is what Fabricius, the tool we create, aims to. His goal is to help at its best to create your projects easily.

## Why not just use CookieCutter or Copier instead of creating your own tool?

See goals, but other than that,

It's a question I am expecting with fears, I tried to first use CookieCutter myself but I never liked it at all, it always broke with me and was painful to use. On top of that, it does not comes with crucial things I would personally require, such as basic type checking when gathering user's input.
As for Copier, while it seems like a much more grown-up tool and *actually* fitting my need, I honestly did not try it, I just lost interested towards it and wanted to challenge myself in creating a new tool for the Python ecosystem.

On top of all of these, during my work in 2022, I ended up using TypeScript and using AdonisJS's CLI tool, and its awesome [template generator](https://docs.adonisjs.com/guides/ace-commandline#templates-generator), and so it made me really interested into creating a project scaffolder but using code, not a directory structure, which was lacking for both tools.

I wanted to create a complete and customizable experience of project scaffolding, I wanted to allow users to be free of do whatever they've meant to do, it's how I came up with the idea of plugins.

To me, Fabricius is more than just a simple project scaffolder, it's a complete handy swiss knife for their users. :)
