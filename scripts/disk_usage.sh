#!/bin/bash

df -h | grep -w vda1 | awk -F'[ %]+' '{print $5}'