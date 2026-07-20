---
date: 2025-07-31
tags: 
title: git reflog might save you
author:
  - Mark Molea
---
Have you ever performed a `git rebase` and realized you made a huge mistake?  Have you even deleted a branch by mistake?  If none of your changes have been pushed to a remote repo, this could mean you've lost a tremendous amount of work.

Luckily, you can recover from those situations using the `git reflog`.  

> **git-reflog**
> 
> This command manages the information recorded in the reflogs.
> 
> Reference logs, or "reflogs", record when the tips of branches and other references were updated in the local repository. Reflogs are useful in various Git commands, to specify the old value of a reference. For example, `HEAD@{2}` means "where HEAD used to be two moves ago", `master@{one.week.ago}` means "where master used to point to one week ago in this local repository", and so on. See [gitrevisions[7]](https://git-scm.com/docs/gitrevisions) for more details.
> 
> source: https://git-scm.com/docs/git-reflog

Just like with `git log`, `reflog` has a SHA for each entry.  These SHA's can be used just like the commit SHA's in your `log`.  You can use commands like `checkout` or  `reset` with the SHA's from `reflog` to interact with your repository at essentially any point in your recent history.  So if you want to undo that `rebase` operation you just performed, you can use `reflog` to find a point in time before the `rebase` and use `reset --hard` to undo the `rebase`.  You could also create a branch based on that state of your repository.  The former would look like this:

```shell
git checkout feature/123
Switched to branch 'feature/123'
Your branch is up to date with 'origin/feature/123'.

git log --oneline -n10
817adf9 (HEAD -> feature/123, origin/feature/123) PROJ-123: Add widget export option
0b05d80 PROJ-119: Exclude duplicates from summary view (#103)
5c355de PROJ-115: Add abbreviation to mapping script (#102)
37b0f1d PROJ-113: Add validation alert indicators (#101)
a543448 PROJ-112: Fix line count bug in file summary view (#100)
1654dc1 PROJ-110: Add supporting tables for reprocessing requests (#99)
56f439d PROJ-105: Add migration script for partner file expectations (#95)
148358f PROJ-107: Clear maintenance flags from batch lines (#98)
dc30e73 PROJ-108: Add forecast example (#96)
700a7d7 PROJ-109: Bulk identifiers insert (#97)

git rebase origin/main
Successfully rebased and updated refs/heads/feature/123.

git log --oneline -n10
3f216c6 (HEAD -> feature/123) PROJ-123: Add widget export option
21bd78c (origin/main, origin/HEAD, main) PROJ-127: Add code mappings (part 1) (#105)
b068156 PROJ-159: Add launch view (#111)
15148ad PROJ-151: Create data connections table (#110)
1a186e6 PROJ-139: Change log entries ID from int to guid (#109)
b22965e PROJ-143: Ensure blocked locations appear in consolidated view (#108)
ee11334 PROJ-137: Add recipient configs table (#107)
457060c PROJ-130: Adjust backout sprocs to delete from staging tables (#106)
4f02b4b PROJ-126: Added load time to invalid identifiers (#104)
0b05d80 PROJ-119: Exclude duplicates from summary view (#103)

git reflog -n10
3f216c6 (HEAD -> feature/123) HEAD@{0}: rebase (finish): returning to refs/heads/feature/123
3f216c6 (HEAD -> feature/123) HEAD@{1}: rebase (pick): PROJ-123: Add widget export option
21bd78c (origin/main, origin/HEAD, main) HEAD@{2}: rebase (start): checkout origin/main
817adf9 (origin/feature/123) HEAD@{3}: checkout: moving from main to feature/123
21bd78c (origin/main, origin/HEAD, main) HEAD@{4}: pull: Fast-forward
15148ad HEAD@{5}: checkout: moving from feature/159 to main
6e2041f HEAD@{6}: commit: PROJ-159: Filter on partner abbreviation instead of name
93bfb0b HEAD@{7}: checkout: moving from main to feature/159
15148ad HEAD@{8}: checkout: moving from feature/159 to main
93bfb0b HEAD@{9}: commit: PROJ-159: Expand log entries value columns to max varchar

git reset --hard 817adf9
HEAD is now at 817adf9 PROJ-123: Add widget export option

git log --oneline -n10
817adf9 (HEAD -> feature/123, origin/feature/123) PROJ-123: Add widget export option
0b05d80 PROJ-119: Exclude duplicates from summary view (#103)
5c355de PROJ-115: Add abbreviation to mapping script (#102)
37b0f1d PROJ-113: Add validation alert indicators (#101)
a543448 PROJ-112: Fix line count bug in file summary view (#100)
1654dc1 PROJ-110: Add supporting tables for reprocessing requests (#99)
56f439d PROJ-105: Add migration script for partner file expectations (#95)
148358f PROJ-107: Clear maintenance flags from batch lines (#98)
dc30e73 PROJ-108: Add forecast example (#96)
700a7d7 PROJ-109: Bulk identifiers insert (#97)

```

In the snippet above we:

1. checked out the `feature/123` branch
2. rebased it with `origin/main`
3. used `reflog` to identify the SHA before the rebase
4. reset our local branch to the point immediately before the `rebase`
5. observe that the history of our branch is ended an identical state to when we initially checked out `VMP-380`

Hope this saves you some grief in the future.  I know it has saved me many times.

> **Closing Thoughts...**
> Remember, creating branches in Git is effectively free.  
> 
> When in doubt, make a new branch to experiment with.  
> 
> You can always cherry-pick your changes over to your real branch if you want those exact commits or delete the experimental branch when you're done.