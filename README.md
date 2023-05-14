# Fabricius

Fabricius - A Python 3.10 Project Template engine with superpowers!

> :warning: Fabricius is a work in progress! Please, play with it with a grain of salt; expect bugs, crashes, non-documented portion of the application & more unexpected behavior.

Documentation: <https://fabricius.readthedocs.io>

> :warning: Fabricius still does not comes with it's CLI tool! It is a work in progress!

## 👀 How about checking out the `development` branch?

This branch has been silent for quite a while now, you might believe the project is dead. **IT'S NOT!**
The true magic is happening behind the scene, available in the `development` branch! If you want to see how things are working out for Fabricius, you should check the stuff out there!

The `master` is here to represent the version of Fabricius that is available on PyPi (As of today, `0.1.0`)

## Goals:

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
