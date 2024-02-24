/* eslint-disable */
import * as types from './graphql';
import { TypedDocumentNode as DocumentNode } from '@graphql-typed-document-node/core';

/**
 * Map of all GraphQL operations in the project.
 *
 * This map has several performance disadvantages:
 * 1. It is not tree-shakeable, so it will include all operations in the project.
 * 2. It is not minifiable, so the string of a GraphQL query will be multiple times inside the bundle.
 * 3. It does not support dead code elimination, so it will add unused operations.
 *
 * Therefore it is highly recommended to use the babel or swc plugin for production.
 */
const documents = {
    "\n    query renderedAvatar($avatar: AvatarInput!) {\n      avatarApi {\n        create(avatar: $avatar) {\n          svg\n        }\n      }\n    }\n  ": types.RenderedAvatarDocument,
    "\n    query avatarParts {\n      avatarApi {\n        tops {\n          ...avatarPart\n        }\n        accessories {\n          ...avatarPart\n        }\n        eyebrows {\n          ...avatarPart\n        }\n        eyes {\n          ...avatarPart\n        }\n        noses {\n          ...avatarPart\n        }\n        mouths {\n          ...avatarPart\n        }\n        beards {\n          ...avatarPart\n        }\n        clothings {\n          ...avatarPart\n        }\n        graphics {\n          ...avatarPart\n        }\n      }\n    }\n    fragment avatarPart on AvatarPart {\n      name\n      svg\n    }\n  ": types.AvatarPartsDocument,
    "\n    query randomAvatar {\n      avatarApi {\n        random {\n          top {\n            name\n          }\n          accessory {\n            name\n          }\n          eyebrows {\n            name\n          }\n          eyes {\n            name\n          }\n          nose {\n            name\n          }\n          mouth {\n            name\n          }\n          beard {\n            name\n          }\n          clothing {\n            name\n          }\n          graphic {\n            name\n          }\n          skinColor\n          hairColor\n          beardColor\n          hatColor\n          clothingColor\n          backgroundColor\n          shirtText\n        }\n      }\n    }\n  ": types.RandomAvatarDocument,
    "\n  query getProjects {\n    projects {\n      dbId\n      name\n      parent {\n        dbId\n      }\n    }\n  }\n": types.GetProjectsDocument,
    "\n    query getTeams {\n        teams {\n            name\n            dbId\n        }\n    }\n": types.GetTeamsDocument,
    "\n  query getUsers {\n    users {\n      dbId\n      name\n      fullName\n      renderedAvatar\n    }\n  }\n": types.GetUsersDocument,
    "\n    query getProjectBoard($dbId: Int!) {\n      project: dbNode(typename: \"Project\", dbId: $dbId) {\n        __typename\n        ... on Project {\n          id\n          name\n          tasks {\n            id\n            dbId\n            name\n            parent {\n              dbId\n            }\n            tags {\n              text\n              color\n            }\n            state\n            finishedAt\n            orderId\n            attached\n            progress {\n              pessimistic\n              average\n              optimistic\n              active\n            }\n            priority\n          }\n          priorities {\n            key\n            text\n            color\n          }\n        }\n      }\n    }\n  ": types.GetProjectBoardDocument,
    "\n  mutation moveTasks($projectDbId: Int!, $state: TaskState!, $tasks: [MovedTaskInput!]!) {\n    project {\n      movedTasks(projectDbId: $projectDbId, state: $state, tasks: $tasks) {\n        success\n      }\n    }\n  }\n": types.MoveTasksDocument,
    "\n    query getProject($dbId: Int!) {\n      project: dbNode(typename: \"Project\", dbId: $dbId) {\n        ... on Project {\n          name\n          children(recursive: true) {\n            dbId\n            name\n            parent {\n              dbId\n            }\n          }\n          parents {\n            dbId\n            name\n          }\n        }\n      }\n    }\n  ": types.GetProjectDocument,
    "\n    query getTaskActivity($dbId: Int!) {\n        task: dbNode(typename: \"Task\", dbId: $dbId) {\n            ... on Task {\n                activity {\n                    __typename\n                    timestamp\n                    ... on TaskActivityEstimateAdded {\n                        estimate { \n                            estimateType { name } \n                            estimatedDuration\n                            expectationOptimistic\n                            expectationPessimistic\n                            expectationAverage\n                        }\n                        user {\n                            name\n                            fullName\n                        }\n                    }\n                    ... on TaskActivityWorkperiod {\n                        duration\n                        user {\n                            name\n                            fullName\n                        }\n                    }\n                }\n            }\n        }\n    }\n  ": types.GetTaskActivityDocument,
    "\n    query getTaskOverview($dbId: Int!) {\n        task: dbNode(typename: \"Task\", dbId: $dbId) {\n            __typename\n            ... on Task {\n                name\n                description\n                state\n                priority\n                type\n                project {\n                    priorities {\n                        key\n                        text\n                        color\n                    }\n                    taskStates {\n                        key\n                        text\n                        color\n                    }\n                    taskTypes {\n                        key\n                        text\n                        color\n                    }\n                }\n                tags {\n                    text\n                    color\n                }\n                workPeriods {\n                    startedAt\n                    endedAt\n                    duration\n                    user {\n                        id\n                        name\n                        fullName\n                        avatar {svg}\n                    }\n                }\n                schedule {\n                    assignee {\n                        id\n                        name\n                        fullName\n                        avatar {svg}\n                    }\n                    average {\n                        start\n                        end\n                    }\n                    optimistic {\n                        start\n                        end\n                    }\n                    pessimistic {\n                        start\n                        end\n                    }\n                }\n                estimates {\n                    user {\n                        id\n                        name\n                        fullName\n                        avatar {svg}\n                    }\n                    estimatedDuration\n                    expectationAverage\n                    expectationOptimistic\n                    expectationPessimistic\n                    estimateType {name}\n                }\n            }\n        }\n    }\n  ": types.GetTaskOverviewDocument,
    "\n    query getTeam($dbId: Int!) {\n      team: dbNode(typename: \"Team\", dbId: $dbId) {\n        ... on Team {\n          name\n          dbId\n          assignedRoles {\n            role {\n              dbId\n              name\n            }\n            user {\n              dbId\n              name\n              fullName\n              renderedAvatar\n            }\n          }\n        }\n      }\n    }\n  ": types.GetTeamDocument,
    "\n    query getTeamNames($dbId: Int!) {\n      dbNode(typename: \"Team\", dbId: $dbId) {\n        ... on Team {\n          name\n        }\n      }\n    }\n  ": types.GetTeamNamesDocument,
    "\n    query schedule(\n      $start: DateTime!\n      $end: DateTime!\n      $mode: ScheduleMode!\n      $dbId: Int!\n    ) {\n      team: dbNode(typename: \"Team\", dbId: $dbId) {\n        __typename\n        ... on Team {\n          id\n          dbId\n          name\n          schedule(input: { start: $start, end: $end, mode: $mode }) {\n            now\n            covers {\n              start\n              end\n            }\n            actual {\n              start\n              end\n            }\n            userSchedules {\n              user {\n                fullName\n              }\n              workingPeriods {\n                start\n                end\n              }\n              timesinks {\n                period {\n                  start\n                  end\n                }\n                color\n                text\n              }\n              workedTasks {\n                period {\n                  start\n                  end\n                }\n                color\n                text\n              }\n              scheduledTasks {\n                period {\n                  start\n                  end\n                }\n                color\n                text\n              }\n            }\n          }\n        }\n      }\n    }\n  ": types.ScheduleDocument,
    "\n    query getUserActivity($dbId: Int!) {\n      user: dbNode(typename: \"User\", dbId: $dbId) {\n        ... on User {\n          activity {\n            at\n            short\n            details\n          }\n        }\n      }\n    }\n  ": types.GetUserActivityDocument,
    "\n    query getUser($dbId: Int!) {\n      user: dbNode(typename: \"User\", dbId: $dbId) {\n        ... on User {\n          name\n          fullName\n          renderedAvatar\n          projectSummaries {\n            project {\n              id\n              dbId\n              name\n            }\n            totalDuration\n            numTasksOpen\n            numTasksDone\n          }\n          estimateStatistics {\n            evaluated\n            numDatapoints\n            shiftOptimistic\n            shiftAverage\n            shiftPessimistic\n            estimateType {\n              name\n              description\n              minDatapoints\n              maxDatapoints\n              relative\n            }\n            sufficient\n            datapoints {\n              value\n              actualWork\n              numWorkPeriods\n              start\n              end\n              estimate {\n                dbId\n                task {\n                  dbId\n                  name\n                }\n                estimatedDuration\n              }\n            }\n          }\n        }\n      }\n    }\n  ": types.GetUserDocument,
    "\n    query user($userId: Int!) {\n      user: dbNode(typename: \"User\", dbId: $userId) {\n        ... on User {\n          name\n          fullName\n          avatar {\n            top {\n              name\n            }\n            accessory {\n              name\n            }\n            eyebrows {\n              name\n            }\n            eyes {\n              name\n            }\n            nose {\n              name\n            }\n            mouth {\n              name\n            }\n            beard {\n              name\n            }\n            clothing {\n              name\n            }\n            graphic {\n              name\n            }\n            skinColor\n            hairColor\n            beardColor\n            hatColor\n            clothingColor\n            backgroundColor\n            shirtText\n          }\n        }\n      }\n    }\n  ": types.UserDocument,
    "\n    mutation saveUser($userId: Int!, $user: UserInput!) {\n      user {\n        update(userId: $userId, user: $user) {\n          success\n        }\n      }\n    }\n  ": types.SaveUserDocument,
};

/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 *
 *
 * @example
 * ```ts
 * const query = graphql(`query GetUser($id: ID!) { user(id: $id) { name } }`);
 * ```
 *
 * The query argument is unknown!
 * Please regenerate the types.
 */
export function graphql(source: string): unknown;

/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n    query renderedAvatar($avatar: AvatarInput!) {\n      avatarApi {\n        create(avatar: $avatar) {\n          svg\n        }\n      }\n    }\n  "): (typeof documents)["\n    query renderedAvatar($avatar: AvatarInput!) {\n      avatarApi {\n        create(avatar: $avatar) {\n          svg\n        }\n      }\n    }\n  "];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n    query avatarParts {\n      avatarApi {\n        tops {\n          ...avatarPart\n        }\n        accessories {\n          ...avatarPart\n        }\n        eyebrows {\n          ...avatarPart\n        }\n        eyes {\n          ...avatarPart\n        }\n        noses {\n          ...avatarPart\n        }\n        mouths {\n          ...avatarPart\n        }\n        beards {\n          ...avatarPart\n        }\n        clothings {\n          ...avatarPart\n        }\n        graphics {\n          ...avatarPart\n        }\n      }\n    }\n    fragment avatarPart on AvatarPart {\n      name\n      svg\n    }\n  "): (typeof documents)["\n    query avatarParts {\n      avatarApi {\n        tops {\n          ...avatarPart\n        }\n        accessories {\n          ...avatarPart\n        }\n        eyebrows {\n          ...avatarPart\n        }\n        eyes {\n          ...avatarPart\n        }\n        noses {\n          ...avatarPart\n        }\n        mouths {\n          ...avatarPart\n        }\n        beards {\n          ...avatarPart\n        }\n        clothings {\n          ...avatarPart\n        }\n        graphics {\n          ...avatarPart\n        }\n      }\n    }\n    fragment avatarPart on AvatarPart {\n      name\n      svg\n    }\n  "];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n    query randomAvatar {\n      avatarApi {\n        random {\n          top {\n            name\n          }\n          accessory {\n            name\n          }\n          eyebrows {\n            name\n          }\n          eyes {\n            name\n          }\n          nose {\n            name\n          }\n          mouth {\n            name\n          }\n          beard {\n            name\n          }\n          clothing {\n            name\n          }\n          graphic {\n            name\n          }\n          skinColor\n          hairColor\n          beardColor\n          hatColor\n          clothingColor\n          backgroundColor\n          shirtText\n        }\n      }\n    }\n  "): (typeof documents)["\n    query randomAvatar {\n      avatarApi {\n        random {\n          top {\n            name\n          }\n          accessory {\n            name\n          }\n          eyebrows {\n            name\n          }\n          eyes {\n            name\n          }\n          nose {\n            name\n          }\n          mouth {\n            name\n          }\n          beard {\n            name\n          }\n          clothing {\n            name\n          }\n          graphic {\n            name\n          }\n          skinColor\n          hairColor\n          beardColor\n          hatColor\n          clothingColor\n          backgroundColor\n          shirtText\n        }\n      }\n    }\n  "];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  query getProjects {\n    projects {\n      dbId\n      name\n      parent {\n        dbId\n      }\n    }\n  }\n"): (typeof documents)["\n  query getProjects {\n    projects {\n      dbId\n      name\n      parent {\n        dbId\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n    query getTeams {\n        teams {\n            name\n            dbId\n        }\n    }\n"): (typeof documents)["\n    query getTeams {\n        teams {\n            name\n            dbId\n        }\n    }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  query getUsers {\n    users {\n      dbId\n      name\n      fullName\n      renderedAvatar\n    }\n  }\n"): (typeof documents)["\n  query getUsers {\n    users {\n      dbId\n      name\n      fullName\n      renderedAvatar\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n    query getProjectBoard($dbId: Int!) {\n      project: dbNode(typename: \"Project\", dbId: $dbId) {\n        __typename\n        ... on Project {\n          id\n          name\n          tasks {\n            id\n            dbId\n            name\n            parent {\n              dbId\n            }\n            tags {\n              text\n              color\n            }\n            state\n            finishedAt\n            orderId\n            attached\n            progress {\n              pessimistic\n              average\n              optimistic\n              active\n            }\n            priority\n          }\n          priorities {\n            key\n            text\n            color\n          }\n        }\n      }\n    }\n  "): (typeof documents)["\n    query getProjectBoard($dbId: Int!) {\n      project: dbNode(typename: \"Project\", dbId: $dbId) {\n        __typename\n        ... on Project {\n          id\n          name\n          tasks {\n            id\n            dbId\n            name\n            parent {\n              dbId\n            }\n            tags {\n              text\n              color\n            }\n            state\n            finishedAt\n            orderId\n            attached\n            progress {\n              pessimistic\n              average\n              optimistic\n              active\n            }\n            priority\n          }\n          priorities {\n            key\n            text\n            color\n          }\n        }\n      }\n    }\n  "];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  mutation moveTasks($projectDbId: Int!, $state: TaskState!, $tasks: [MovedTaskInput!]!) {\n    project {\n      movedTasks(projectDbId: $projectDbId, state: $state, tasks: $tasks) {\n        success\n      }\n    }\n  }\n"): (typeof documents)["\n  mutation moveTasks($projectDbId: Int!, $state: TaskState!, $tasks: [MovedTaskInput!]!) {\n    project {\n      movedTasks(projectDbId: $projectDbId, state: $state, tasks: $tasks) {\n        success\n      }\n    }\n  }\n"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n    query getProject($dbId: Int!) {\n      project: dbNode(typename: \"Project\", dbId: $dbId) {\n        ... on Project {\n          name\n          children(recursive: true) {\n            dbId\n            name\n            parent {\n              dbId\n            }\n          }\n          parents {\n            dbId\n            name\n          }\n        }\n      }\n    }\n  "): (typeof documents)["\n    query getProject($dbId: Int!) {\n      project: dbNode(typename: \"Project\", dbId: $dbId) {\n        ... on Project {\n          name\n          children(recursive: true) {\n            dbId\n            name\n            parent {\n              dbId\n            }\n          }\n          parents {\n            dbId\n            name\n          }\n        }\n      }\n    }\n  "];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n    query getTaskActivity($dbId: Int!) {\n        task: dbNode(typename: \"Task\", dbId: $dbId) {\n            ... on Task {\n                activity {\n                    __typename\n                    timestamp\n                    ... on TaskActivityEstimateAdded {\n                        estimate { \n                            estimateType { name } \n                            estimatedDuration\n                            expectationOptimistic\n                            expectationPessimistic\n                            expectationAverage\n                        }\n                        user {\n                            name\n                            fullName\n                        }\n                    }\n                    ... on TaskActivityWorkperiod {\n                        duration\n                        user {\n                            name\n                            fullName\n                        }\n                    }\n                }\n            }\n        }\n    }\n  "): (typeof documents)["\n    query getTaskActivity($dbId: Int!) {\n        task: dbNode(typename: \"Task\", dbId: $dbId) {\n            ... on Task {\n                activity {\n                    __typename\n                    timestamp\n                    ... on TaskActivityEstimateAdded {\n                        estimate { \n                            estimateType { name } \n                            estimatedDuration\n                            expectationOptimistic\n                            expectationPessimistic\n                            expectationAverage\n                        }\n                        user {\n                            name\n                            fullName\n                        }\n                    }\n                    ... on TaskActivityWorkperiod {\n                        duration\n                        user {\n                            name\n                            fullName\n                        }\n                    }\n                }\n            }\n        }\n    }\n  "];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n    query getTaskOverview($dbId: Int!) {\n        task: dbNode(typename: \"Task\", dbId: $dbId) {\n            __typename\n            ... on Task {\n                name\n                description\n                state\n                priority\n                type\n                project {\n                    priorities {\n                        key\n                        text\n                        color\n                    }\n                    taskStates {\n                        key\n                        text\n                        color\n                    }\n                    taskTypes {\n                        key\n                        text\n                        color\n                    }\n                }\n                tags {\n                    text\n                    color\n                }\n                workPeriods {\n                    startedAt\n                    endedAt\n                    duration\n                    user {\n                        id\n                        name\n                        fullName\n                        avatar {svg}\n                    }\n                }\n                schedule {\n                    assignee {\n                        id\n                        name\n                        fullName\n                        avatar {svg}\n                    }\n                    average {\n                        start\n                        end\n                    }\n                    optimistic {\n                        start\n                        end\n                    }\n                    pessimistic {\n                        start\n                        end\n                    }\n                }\n                estimates {\n                    user {\n                        id\n                        name\n                        fullName\n                        avatar {svg}\n                    }\n                    estimatedDuration\n                    expectationAverage\n                    expectationOptimistic\n                    expectationPessimistic\n                    estimateType {name}\n                }\n            }\n        }\n    }\n  "): (typeof documents)["\n    query getTaskOverview($dbId: Int!) {\n        task: dbNode(typename: \"Task\", dbId: $dbId) {\n            __typename\n            ... on Task {\n                name\n                description\n                state\n                priority\n                type\n                project {\n                    priorities {\n                        key\n                        text\n                        color\n                    }\n                    taskStates {\n                        key\n                        text\n                        color\n                    }\n                    taskTypes {\n                        key\n                        text\n                        color\n                    }\n                }\n                tags {\n                    text\n                    color\n                }\n                workPeriods {\n                    startedAt\n                    endedAt\n                    duration\n                    user {\n                        id\n                        name\n                        fullName\n                        avatar {svg}\n                    }\n                }\n                schedule {\n                    assignee {\n                        id\n                        name\n                        fullName\n                        avatar {svg}\n                    }\n                    average {\n                        start\n                        end\n                    }\n                    optimistic {\n                        start\n                        end\n                    }\n                    pessimistic {\n                        start\n                        end\n                    }\n                }\n                estimates {\n                    user {\n                        id\n                        name\n                        fullName\n                        avatar {svg}\n                    }\n                    estimatedDuration\n                    expectationAverage\n                    expectationOptimistic\n                    expectationPessimistic\n                    estimateType {name}\n                }\n            }\n        }\n    }\n  "];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n    query getTeam($dbId: Int!) {\n      team: dbNode(typename: \"Team\", dbId: $dbId) {\n        ... on Team {\n          name\n          dbId\n          assignedRoles {\n            role {\n              dbId\n              name\n            }\n            user {\n              dbId\n              name\n              fullName\n              renderedAvatar\n            }\n          }\n        }\n      }\n    }\n  "): (typeof documents)["\n    query getTeam($dbId: Int!) {\n      team: dbNode(typename: \"Team\", dbId: $dbId) {\n        ... on Team {\n          name\n          dbId\n          assignedRoles {\n            role {\n              dbId\n              name\n            }\n            user {\n              dbId\n              name\n              fullName\n              renderedAvatar\n            }\n          }\n        }\n      }\n    }\n  "];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n    query getTeamNames($dbId: Int!) {\n      dbNode(typename: \"Team\", dbId: $dbId) {\n        ... on Team {\n          name\n        }\n      }\n    }\n  "): (typeof documents)["\n    query getTeamNames($dbId: Int!) {\n      dbNode(typename: \"Team\", dbId: $dbId) {\n        ... on Team {\n          name\n        }\n      }\n    }\n  "];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n    query schedule(\n      $start: DateTime!\n      $end: DateTime!\n      $mode: ScheduleMode!\n      $dbId: Int!\n    ) {\n      team: dbNode(typename: \"Team\", dbId: $dbId) {\n        __typename\n        ... on Team {\n          id\n          dbId\n          name\n          schedule(input: { start: $start, end: $end, mode: $mode }) {\n            now\n            covers {\n              start\n              end\n            }\n            actual {\n              start\n              end\n            }\n            userSchedules {\n              user {\n                fullName\n              }\n              workingPeriods {\n                start\n                end\n              }\n              timesinks {\n                period {\n                  start\n                  end\n                }\n                color\n                text\n              }\n              workedTasks {\n                period {\n                  start\n                  end\n                }\n                color\n                text\n              }\n              scheduledTasks {\n                period {\n                  start\n                  end\n                }\n                color\n                text\n              }\n            }\n          }\n        }\n      }\n    }\n  "): (typeof documents)["\n    query schedule(\n      $start: DateTime!\n      $end: DateTime!\n      $mode: ScheduleMode!\n      $dbId: Int!\n    ) {\n      team: dbNode(typename: \"Team\", dbId: $dbId) {\n        __typename\n        ... on Team {\n          id\n          dbId\n          name\n          schedule(input: { start: $start, end: $end, mode: $mode }) {\n            now\n            covers {\n              start\n              end\n            }\n            actual {\n              start\n              end\n            }\n            userSchedules {\n              user {\n                fullName\n              }\n              workingPeriods {\n                start\n                end\n              }\n              timesinks {\n                period {\n                  start\n                  end\n                }\n                color\n                text\n              }\n              workedTasks {\n                period {\n                  start\n                  end\n                }\n                color\n                text\n              }\n              scheduledTasks {\n                period {\n                  start\n                  end\n                }\n                color\n                text\n              }\n            }\n          }\n        }\n      }\n    }\n  "];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n    query getUserActivity($dbId: Int!) {\n      user: dbNode(typename: \"User\", dbId: $dbId) {\n        ... on User {\n          activity {\n            at\n            short\n            details\n          }\n        }\n      }\n    }\n  "): (typeof documents)["\n    query getUserActivity($dbId: Int!) {\n      user: dbNode(typename: \"User\", dbId: $dbId) {\n        ... on User {\n          activity {\n            at\n            short\n            details\n          }\n        }\n      }\n    }\n  "];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n    query getUser($dbId: Int!) {\n      user: dbNode(typename: \"User\", dbId: $dbId) {\n        ... on User {\n          name\n          fullName\n          renderedAvatar\n          projectSummaries {\n            project {\n              id\n              dbId\n              name\n            }\n            totalDuration\n            numTasksOpen\n            numTasksDone\n          }\n          estimateStatistics {\n            evaluated\n            numDatapoints\n            shiftOptimistic\n            shiftAverage\n            shiftPessimistic\n            estimateType {\n              name\n              description\n              minDatapoints\n              maxDatapoints\n              relative\n            }\n            sufficient\n            datapoints {\n              value\n              actualWork\n              numWorkPeriods\n              start\n              end\n              estimate {\n                dbId\n                task {\n                  dbId\n                  name\n                }\n                estimatedDuration\n              }\n            }\n          }\n        }\n      }\n    }\n  "): (typeof documents)["\n    query getUser($dbId: Int!) {\n      user: dbNode(typename: \"User\", dbId: $dbId) {\n        ... on User {\n          name\n          fullName\n          renderedAvatar\n          projectSummaries {\n            project {\n              id\n              dbId\n              name\n            }\n            totalDuration\n            numTasksOpen\n            numTasksDone\n          }\n          estimateStatistics {\n            evaluated\n            numDatapoints\n            shiftOptimistic\n            shiftAverage\n            shiftPessimistic\n            estimateType {\n              name\n              description\n              minDatapoints\n              maxDatapoints\n              relative\n            }\n            sufficient\n            datapoints {\n              value\n              actualWork\n              numWorkPeriods\n              start\n              end\n              estimate {\n                dbId\n                task {\n                  dbId\n                  name\n                }\n                estimatedDuration\n              }\n            }\n          }\n        }\n      }\n    }\n  "];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n    query user($userId: Int!) {\n      user: dbNode(typename: \"User\", dbId: $userId) {\n        ... on User {\n          name\n          fullName\n          avatar {\n            top {\n              name\n            }\n            accessory {\n              name\n            }\n            eyebrows {\n              name\n            }\n            eyes {\n              name\n            }\n            nose {\n              name\n            }\n            mouth {\n              name\n            }\n            beard {\n              name\n            }\n            clothing {\n              name\n            }\n            graphic {\n              name\n            }\n            skinColor\n            hairColor\n            beardColor\n            hatColor\n            clothingColor\n            backgroundColor\n            shirtText\n          }\n        }\n      }\n    }\n  "): (typeof documents)["\n    query user($userId: Int!) {\n      user: dbNode(typename: \"User\", dbId: $userId) {\n        ... on User {\n          name\n          fullName\n          avatar {\n            top {\n              name\n            }\n            accessory {\n              name\n            }\n            eyebrows {\n              name\n            }\n            eyes {\n              name\n            }\n            nose {\n              name\n            }\n            mouth {\n              name\n            }\n            beard {\n              name\n            }\n            clothing {\n              name\n            }\n            graphic {\n              name\n            }\n            skinColor\n            hairColor\n            beardColor\n            hatColor\n            clothingColor\n            backgroundColor\n            shirtText\n          }\n        }\n      }\n    }\n  "];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n    mutation saveUser($userId: Int!, $user: UserInput!) {\n      user {\n        update(userId: $userId, user: $user) {\n          success\n        }\n      }\n    }\n  "): (typeof documents)["\n    mutation saveUser($userId: Int!, $user: UserInput!) {\n      user {\n        update(userId: $userId, user: $user) {\n          success\n        }\n      }\n    }\n  "];

export function graphql(source: string) {
  return (documents as any)[source] ?? {};
}

export type DocumentType<TDocumentNode extends DocumentNode<any, any>> = TDocumentNode extends DocumentNode<  infer TType,  any>  ? TType  : never;