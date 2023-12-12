#!/usr/local/cs/bin/python3

# strace -f -o topo-test.tr pytest allows the user to view all of the processes created during the program's run
    # can manually parse through the calls to see that only open, read, access, close, etc are called
    # no external commands are called
# to confirm
    # topo-test.tr | grep "git" > a.txt
    # topo-test.tr | grep "execve" > a.txt
    # confirms no external git commands were called

import os
import sys
import zlib
import copy
from collections import deque

def topo_order_commits():
    git_directory = get_git_directory()
    branch_names = get_local_branch_names(git_directory)

    commit_hashes = []

    for branch_name in branch_names:
        file_path = os.path.join(git_directory, '.git', 'refs', 'heads', branch_name)

        if os.path.isfile(file_path):
            with open(file_path, 'r') as f:
                commit_hashes.append(f.readline().strip())

    commit_graph = build_commit_graph(git_directory, commit_hashes)

    # for commit_hash, commit_node in commit_graph.items():
    #     print(f"commit Hash: {commit_hash}")
    #     print(f"parents: {commit_node.parents}")
    #     print(f"children: {commit_node.children}")
    #     print()

    sorted_commits = topological_sort(commit_graph)
    # print("sorted commits:", sorted_commits)

    head_to_branches = generate_head_to_branches(git_directory, branch_names)
    print_topo_ordered_commits_with_branch_names(commit_graph, sorted_commits, head_to_branches)

def get_git_directory():
    # start searching from the location wherever the code was called in
    current_path = os.getcwd()

    while current_path != '/':
        git_path = os.path.join(current_path, '.git')

        # if the .git directory exists in that folder, great you found it!
        if os.path.exists(git_path):
            return current_path

        # else, go up a level to the parent directory and repeat
        current_path = os.path.dirname(current_path)

    # you should stop the search when you reach the root directory '/'
    print("Not inside a Git repository", file=sys.stderr)
    sys.exit(1)

def get_local_branch_names(git_directory):
    # look for:
        # files – file bame is the branch name, contents are the commit it points to
        # folders – these can contain more branches which you need to inspect
    # branch names are stored in the refs/heads folder
    refs_heads_path = os.path.join(git_directory, '.git', 'refs', 'heads')
    return get_local_branch_names_recursive(refs_heads_path)

def get_local_branch_names_recursive(directory, parent_dir=""):
    branch_names = []

    for entry in os.scandir(directory):
        if entry.is_file() and not entry.name.startswith('.'):
            # append the branch name with the parent directory
            branch_name = os.path.join(parent_dir, entry.name)
            branch_names.append(branch_name)
        elif entry.is_dir():
            # recursively get branch names from subdirectories
            subdirectory = os.path.join(directory, entry.name)
            branch_names.extend(get_local_branch_names_recursive(subdirectory, parent_dir=entry.name))

    return branch_names

class CommitNode:
    def __init__(self, commit_hash):
        self.commit_hash = commit_hash
        self.parents = []
        self.children = []

def build_commit_graph(git_dir, local_branch_heads):
    commit_nodes = {} 
    visited = set()
    stack = local_branch_heads

    while stack:
        commit_hash = stack.pop()  
        if commit_hash in visited:
            continue  

        visited.add(commit_hash)

        if commit_hash not in commit_nodes:
            # create a commit node and store it in the graph
            commit_nodes[commit_hash] = CommitNode(commit_hash)

        # using commit_hash, retrieve commit node object from graph
        commit = commit_nodes[commit_hash]

        # find commit_hash in the objects folder, decompress it, and get parent commits
        commit_file_path = os.path.join(git_dir, '.git', 'objects', commit_hash[:2], commit_hash[2:])
        with open(commit_file_path, 'rb') as f:
            decompressed_content = zlib.decompress(f.read()).decode('utf-8')

        # extract parent commits from commit content
        parent_lines = [line.split()[1] for line in decompressed_content.splitlines() if line.startswith('parent')]
        commit.parents = set(parent_lines)

        for p in commit.parents:
            if p not in visited:
                stack.append(p)  # add parent to the processing list if not visited

            if p not in commit_nodes:
                commit_nodes[p] = CommitNode(p)  # create a parent node if not in the graph

            # record that commit_hash is a child of commit node p
            commit_nodes[p].children.insert(0, commit_hash)

    return commit_nodes

def topological_sort(commit_nodes):
    result = []            # commits we have processed and are now sorted
    no_children = deque()  # commits we can process now
    copy_graph = copy.deepcopy(commit_nodes)  # copy graph so we don't erase info
    in_degree = {commit_hash: len(commit_nodes[commit_hash].parents) for commit_hash in copy_graph}

    # if the commit has no children, we can process it
    for commit_hash in copy_graph:
        if in_degree[commit_hash] == 0:
            no_children.append(commit_hash)

    # loop through until all commits are processed
    while len(no_children) > 0:
        commit_hash = no_children.popleft()
        result.insert(0, commit_hash)

        # now that we are processing commit, remove all connecting edges to child commits
        for child_hash in copy_graph[commit_hash].children:
            in_degree[child_hash] -= 1

            # if the child has no more parents, add it to the processing set
            if in_degree[child_hash] == 0:
                no_children.append(child_hash)

    # error check 
    if len(result) < len(commit_nodes):
        raise Exception("cycle detected")

    return result

def generate_head_to_branches(git_directory, branch_names):
    head_to_branches = {}

    for branch_name in branch_names:
        file_path = os.path.join(git_directory, '.git', 'refs', 'heads', branch_name)

        if os.path.isfile(file_path):
            with open(file_path, 'r') as f:
                commit_hash = f.readline().strip()
                # check if commit hash is already a key in head_to_branches
                if commit_hash in head_to_branches:
                    head_to_branches[commit_hash].append(branch_name)
                else:
                    head_to_branches[commit_hash] = [branch_name]

    return head_to_branches

def print_topo_ordered_commits_with_branch_names(commit_nodes, topo_ordered_commits, head_to_branches):
    jumped = False
    for i in range(len(topo_ordered_commits)):
        commit_hash = topo_ordered_commits[i]
        if jumped:
            jumped = False
            sticky_hash = ' '.join(commit_nodes[commit_hash].children)
            print(f'={sticky_hash}')
        branches = sorted(head_to_branches[commit_hash]) if commit_hash in head_to_branches else []
        print(commit_hash + (' ' + ' '.join(branches) if branches else ''))
        if i+1 < len(topo_ordered_commits) and topo_ordered_commits[i+1] not in commit_nodes[commit_hash].parents:
            jumped = True
            sticky_hash = ' '.join(commit_nodes[commit_hash].parents)
            print(f'{sticky_hash}=\n')

if __name__ == '__main__':
    topo_order_commits()